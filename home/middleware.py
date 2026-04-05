import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


RATE_LIMIT_WINDOW_SECONDS = getattr(settings, "CHAT_RATE_LIMIT_WINDOW_SECONDS", 60)
RATE_LIMIT_MAX_REQUESTS = getattr(settings, "CHAT_RATE_LIMIT_MAX_REQUESTS", 12)


class SecurityHeadersMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
		response["Cross-Origin-Opener-Policy"] = "same-origin"
		response["Cross-Origin-Resource-Policy"] = "same-origin"
		response["Cross-Origin-Embedder-Policy"] = "require-corp"
		csp_parts = [
			"default-src 'self'",
			"base-uri 'self'",
			"object-src 'none'",
			"frame-ancestors 'none'",
			"form-action 'self'",
			"img-src 'self' data:",
			"style-src 'self' https://fonts.googleapis.com",
			"font-src 'self' https://fonts.gstatic.com",
			"script-src 'self'",
			"connect-src 'self'",
		]
		if not settings.DEBUG:
			csp_parts.append("upgrade-insecure-requests")

		response["Content-Security-Policy"] = "; ".join(csp_parts)
		return response


class ChatRateLimitMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.path.startswith("/api/chat/"):
			client_ip = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
			if not client_ip:
				client_ip = request.META.get("REMOTE_ADDR", "unknown")

			cache_key = f"chat-rate:{client_ip}"
			now = int(time.time())
			data = cache.get(cache_key)
			if not data or now - data["start"] >= RATE_LIMIT_WINDOW_SECONDS:
				data = {"start": now, "count": 0}

			data["count"] += 1
			cache.set(cache_key, data, RATE_LIMIT_WINDOW_SECONDS)

			if data["count"] > RATE_LIMIT_MAX_REQUESTS:
				return JsonResponse(
					{"error": "Rate limit exceeded. Please wait a minute and try again."},
					status=429,
				)

		return self.get_response(request)
