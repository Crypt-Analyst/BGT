import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Callable

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse

logger = logging.getLogger("home.utils")


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        # X-Forwarded-For may contain a comma-separated list
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def rate_limit(limit: int = 60, period: int = 60):
    """Simple per-IP rate limiter using Django cache.

    Returns 429 HTTP response when limit exceeded. Works for both JSON and HTML endpoints.
    """

    def decorator(view_func: Callable):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            ip = get_client_ip(request) or "unknown"
            key = f"rl:{view_func.__name__}:{ip}"
            try:
                count = cache.get(key, 0)
                if count >= limit:
                    # Decide JSON vs HTML response
                    accepts_json = "application/json" in request.META.get(
                        "HTTP_ACCEPT", ""
                    )
                    if accepts_json or request.headers.get("x-requested-with") == "XMLHttpRequest":
                        return JsonResponse({"error": "Too many requests"}, status=429)
                    return HttpResponse("Too many requests", status=429)
                else:
                    # increment with expiry
                    cache.incr(key)
            except ValueError:
                # Key did not exist; set it
                cache.set(key, 1, timeout=period)
            except Exception as exc:
                logger.exception("Rate limiter cache error: %s", exc)

            # Ensure the key has an expiry set (safe set)
            if cache.get(key) == 1:
                cache.expire(key, period) if hasattr(cache, "expire") else None

            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


# Simple threaded email sender for background delivery (not a replacement for Celery)
_executor = ThreadPoolExecutor(max_workers=2)


def async_send_email(email: EmailMessage):
    """Send `EmailMessage` in background; logs failures."""

    def _send():
        try:
            email.send(fail_silently=False)
            logger.info("Sent email to %s subject=%s", email.to, email.subject)
        except Exception as exc:
            logger.exception("Failed to send email: %s", exc)

    _executor.submit(_send)
