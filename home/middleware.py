import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

try:
    # ipware v4+: provides `get_client_ip` at module root
    from ipware import get_client_ip  # type: ignore
except Exception:
    try:
        # older layout
        from ipware.ip import get_client_ip  # type: ignore
    except Exception:
        # fallback - best-effort stub to avoid crashes if ipware missing
        def get_client_ip(request):
            return (None, False)


logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")

RATE_LIMIT_WINDOW_SECONDS = getattr(settings, "CHAT_RATE_LIMIT_WINDOW_SECONDS", 60)
RATE_LIMIT_MAX_REQUESTS = getattr(settings, "CHAT_RATE_LIMIT_MAX_REQUESTS", 12)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add security headers to all responses."""

    def process_response(self, request, response):
        # Prevent MIME type sniffing
        response["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response["X-Frame-Options"] = "DENY"

        # Control how much referrer information is shared
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (formerly Feature-Policy)
        response["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), usb=()"
        )

        # CORS and origin isolation
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Cross-Origin-Resource-Policy"] = "same-origin"
        response["Cross-Origin-Embedder-Policy"] = "require-corp"

        # Content Security Policy
        csp_parts = [
            "default-src 'self'",
            "base-uri 'self'",
            "object-src 'none'",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "img-src 'self' data: https:",
            "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'",
            "font-src 'self' https://fonts.gstatic.com",
            "script-src 'self' https://cdn.jsdelivr.net https://unpkg.com https://www.googletagmanager.com https://static.hotjar.com",
            "connect-src 'self'",
            "media-src 'self'",
        ]

        if settings.DEBUG:
            csp_parts.extend(
                [
                    "script-src-elem 'self' 'unsafe-inline'",
                    "style-src 'unsafe-inline'",
                ]
            )
        else:
            csp_parts.append("upgrade-insecure-requests")

        response["Content-Security-Policy"] = "; ".join(csp_parts)

        # Additional security headers
        response["X-XSS-Protection"] = "1; mode=block"
        response["X-UA-Compatible"] = "IE=edge"
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


class ChatRateLimitMiddleware(MiddlewareMixin):
    """Rate limiting middleware for chat API endpoint."""

    def process_request(self, request):
        if request.path.startswith("/api/chat/"):
            client_ip, is_routable = get_client_ip(request)

            if not client_ip:
                client_ip = "unknown"

            cache_key = f"chat-rate:{client_ip}"
            now = int(time.time())
            data = cache.get(cache_key)

            if not data or now - data.get("start", 0) >= RATE_LIMIT_WINDOW_SECONDS:
                data = {"start": now, "count": 0}

            data["count"] += 1
            cache.set(cache_key, data, RATE_LIMIT_WINDOW_SECONDS)

            if data["count"] > RATE_LIMIT_MAX_REQUESTS:
                security_logger.warning(
                    f"Rate limit exceeded for IP: {client_ip}",
                    extra={"ip": client_ip, "endpoint": request.path},
                )
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. Please wait a minute and try again.",
                        "retry_after": RATE_LIMIT_WINDOW_SECONDS,
                    },
                    status=429,
                )

        return None


class AuditLoggingMiddleware(MiddlewareMixin):
    """Log important security events."""

    # Paths to log
    SENSITIVE_PATHS = [
        "/admin/",
        "/api/auth/",
        "/api/users/",
        "/api/upload/",
    ]

    def process_request(self, request):
        # Store request start time for logging
        request._audit_start_time = time.time()
        return None

    def process_response(self, request, response):
        # Log sensitive operations
        for path in self.SENSITIVE_PATHS:
            if request.path.startswith(path):
                client_ip, _ = get_client_ip(request)
                duration = time.time() - getattr(
                    request, "_audit_start_time", time.time()
                )

                log_data = {
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "ip": client_ip,
                    "user": str(request.user),
                    "duration": f"{duration:.3f}s",
                }

                if response.status_code >= 400:
                    security_logger.warning(
                        f"API Error: {request.path}", extra=log_data
                    )
                else:
                    logger.info(f"API Call: {request.path}", extra=log_data)

        return response


class SecurityContextMiddleware(MiddlewareMixin):
    """Add security context to request."""

    def process_request(self, request):
        # Add client IP to request
        client_ip, is_routable = get_client_ip(request)
        request.client_ip = client_ip
        request.is_routable_ip = is_routable
        return None


class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """Detect and block potential SQL injection attempts."""

    DANGEROUS_PATTERNS = [
        "'; DROP",
        "'; DELETE",
        "UNION SELECT",
        "OR 1=1",
        "EXEC(",
        "EXECUTE(",
    ]

    def process_request(self, request):
        # Check query parameters
        for value in request.GET.values():
            if isinstance(value, str):
                for pattern in self.DANGEROUS_PATTERNS:
                    if pattern.lower() in value.lower():
                        client_ip, _ = get_client_ip(request)
                        security_logger.critical(
                            f"Potential SQL injection attempt detected",
                            extra={
                                "ip": client_ip,
                                "path": request.path,
                                "pattern": pattern,
                            },
                        )
                        return JsonResponse(
                            {"error": "Invalid request"},
                            status=400,
                        )

        return None
