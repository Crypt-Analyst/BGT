"""Production environment validation and readiness checks."""

import os

from django.conf import settings


def check_production_ready():
    """
    Validate that the Django application is ready for production deployment.
    Returns a dict with checks and any warnings/errors found.
    """
    checks = {
        "status": "ready",
        "warnings": [],
        "errors": [],
    }

    # Security checks
    if settings.DEBUG:
        checks["errors"].append("DEBUG=True in production is a security risk")

    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 50:
        checks["errors"].append("SECRET_KEY is too short or missing (min 50 chars)")

    if not settings.ALLOWED_HOSTS and not settings.DEBUG:
        checks["errors"].append("ALLOWED_HOSTS is empty in production")

    if not settings.SECURE_SSL_REDIRECT and not settings.DEBUG:
        checks["warnings"].append("SECURE_SSL_REDIRECT is disabled in production")

    # Database checks
    if "sqlite" in settings.DATABASES["default"]["ENGINE"] and not settings.DEBUG:
        checks["warnings"].append(
            "SQLite database detected in production (not recommended for production)"
        )

    if not os.getenv("DATABASE_URL") and "sqlite" not in settings.DATABASES["default"]["ENGINE"]:
        checks["errors"].append("DATABASE_URL not set but Postgres is configured")

    # Email checks
    if not settings.EMAIL_HOST_PASSWORD and not settings.DEBUG:
        checks["warnings"].append(
            "EMAIL_HOST_PASSWORD not configured (email sending may fail)"
        )

    # API/Integration checks
    if not settings.OPENAI_API_KEY:
        checks["warnings"].append(
            "OPENAI_API_KEY not set (chat feature will be unavailable)"
        )

    # Celery checks
    if "localhost" in settings.CELERY_BROKER_URL:
        checks["warnings"].append(
            "CELERY_BROKER_URL points to localhost (Redis should be on network/container)"
        )

    # Static files
    if not os.path.exists(settings.STATIC_ROOT) and not settings.DEBUG:
        checks["warnings"].append(
            f"Static files not collected ({settings.STATIC_ROOT} missing)"
        )

    # Sentry
    if not settings.SENTRY_DSN:
        checks["warnings"].append(
            "SENTRY_DSN not configured (error tracking unavailable)"
        )

    # Determine overall status
    if checks["errors"]:
        checks["status"] = "not_ready"
    elif checks["warnings"]:
        checks["status"] = "ready_with_warnings"

    return checks


def get_production_checklist():
    """Return a production deployment checklist."""
    return {
        "pre_deployment": [
            "Set DJANGO_SECRET_KEY to a strong random value (min 50 chars)",
            "Set DJANGO_DEBUG=False",
            "Set DJANGO_ALLOWED_HOSTS to your domain(s)",
            "Configure OPENAI_API_KEY for chat functionality",
            "Set up PostgreSQL database and DATABASE_URL",
            "Configure email credentials (DJANGO_EMAIL_HOST_PASSWORD)",
            "Set up Redis for Celery broker",
            "Run 'python manage.py collectstatic' to gather static files",
            "Run 'python manage.py migrate' to apply database migrations",
            "Configure SENTRY_DSN for error tracking",
        ],
        "infrastructure": [
            "Set up SSL/TLS certificates (use Let's Encrypt for free)",
            "Configure SECURE_SSL_REDIRECT=True",
            "Set SECURE_HSTS_SECONDS to a high value (usually 31536000 for 1 year)",
            "Use a reverse proxy (nginx/Apache) in front of Gunicorn",
            "Set up Redis persistence if using for Celery",
            "Configure log rotation and backups",
            "Set up monitoring and alerting",
        ],
        "docker_deployment": [
            "Build Docker image: docker build -t bgt:latest .",
            "Push to registry: docker push your-registry/bgt:latest",
            "Deploy with docker-compose or Kubernetes",
            "Configure environment variables in production",
            "Set up health checks and auto-restart policies",
            "Configure persistent volumes for logs and media",
        ],
        "post_deployment": [
            "Test the API endpoint (GET /api/)",
            "Test the chat endpoint (POST /api/chat/)",
            "Test contact form submission",
            "Verify email notifications are received",
            "Monitor logs in logs/ directory",
            "Check Django admin at /admin/",
            "Monitor application performance and errors",
        ],
    }
