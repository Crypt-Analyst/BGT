"""
Audit logging system for tracking important security events.
"""

import json
import logging
from typing import Any, Dict, Optional

from django.contrib.auth.models import AnonymousUser, User
from django.db import models
from django.utils import timezone

logger = logging.getLogger("audit")


class AuditLog(models.Model):
    """Model for storing audit logs."""

    # Event types
    EVENT_TYPES = (
        ("login", "User Login"),
        ("logout", "User Logout"),
        ("login_failed", "Failed Login Attempt"),
        ("password_change", "Password Changed"),
        ("password_reset", "Password Reset"),
        ("2fa_enabled", "2FA Enabled"),
        ("2fa_disabled", "2FA Disabled"),
        ("file_upload", "File Uploaded"),
        ("file_download", "File Downloaded"),
        ("data_access", "Data Accessed"),
        ("data_modified", "Data Modified"),
        ("data_deleted", "Data Deleted"),
        ("api_call", "API Call"),
        ("permission_change", "Permission Changed"),
        ("admin_action", "Admin Action"),
        ("security_alert", "Security Alert"),
        ("failed_auth", "Authentication Failed"),
        ("suspicious_activity", "Suspicious Activity"),
    )

    # Severity levels
    SEVERITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="low")
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    session_id = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["event_type", "-timestamp"]),
            models.Index(fields=["ip_address", "-timestamp"]),
            models.Index(fields=["severity", "-timestamp"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} - {self.user} - {self.timestamp}"


class AuditLogManager:
    """Manager for audit logging operations."""

    @staticmethod
    def log_event(
        request,
        event_type: str,
        action: str,
        severity: str = "low",
        data: Optional[Dict[str, Any]] = None,
        error_message: str = "",
    ) -> AuditLog:
        """
        Log an audit event.

        Args:
            request: Django request object
            event_type: Type of event
            action: Description of action
            severity: Severity level (low, medium, high, critical)
            data: Additional data to log
            error_message: Error message if applicable

        Returns:
            Created AuditLog instance
        """
        try:
            from ipware import get_client_ip  # type: ignore
        except Exception:
            try:
                from ipware.ip import get_client_ip  # type: ignore
            except Exception:

                def get_client_ip(req):
                    return (None, False)

        client_ip, is_routable = get_client_ip(request)

        audit_log = AuditLog.objects.create(
            user=request.user if not isinstance(request.user, AnonymousUser) else None,
            event_type=event_type,
            severity=severity,
            action=action,
            ip_address=client_ip or "0.0.0.0",
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            path=request.path,
            method=request.method,
            data=data or {},
            error_message=error_message,
            session_id=request.session.session_key or "",
        )

        # Also log to audit logger
        log_level = {
            "low": logging.INFO,
            "medium": logging.WARNING,
            "high": logging.ERROR,
            "critical": logging.CRITICAL,
        }.get(severity, logging.INFO)

        logger.log(
            log_level,
            f"{event_type}: {action}",
            extra={
                "event_type": event_type,
                "user": str(request.user),
                "ip": client_ip,
                "action": action,
                "data": json.dumps(data or {}),
            },
        )

        return audit_log

    @staticmethod
    def log_login(request, success: bool = True) -> None:
        """
        Log user login event.

        Args:
            request: Django request object
            success: Whether login was successful
        """
        event_type = "login" if success else "login_failed"
        severity = "low" if success else "medium"
        action = f"User login {'successful' if success else 'failed'}"

        AuditLogManager.log_event(
            request,
            event_type=event_type,
            action=action,
            severity=severity,
        )

    @staticmethod
    def log_logout(request) -> None:
        """
        Log user logout event.

        Args:
            request: Django request object
        """
        AuditLogManager.log_event(
            request,
            event_type="logout",
            action="User logged out",
            severity="low",
        )

    @staticmethod
    def log_password_change(request, user: User) -> None:
        """
        Log password change event.

        Args:
            request: Django request object
            user: User who changed password
        """
        AuditLogManager.log_event(
            request,
            event_type="password_change",
            action=f"Password changed for user {user.username}",
            severity="medium",
            data={"user_id": user.id, "username": user.username},
        )

    @staticmethod
    def log_file_upload(
        request,
        filename: str,
        file_size: int,
        content_type: str,
        success: bool = True,
    ) -> None:
        """
        Log file upload event.

        Args:
            request: Django request object
            filename: Name of uploaded file
            file_size: Size of file in bytes
            content_type: MIME type of file
            success: Whether upload was successful
        """
        AuditLogManager.log_event(
            request,
            event_type="file_upload",
            action=f"File uploaded: {filename}",
            severity="low" if success else "medium",
            data={
                "filename": filename,
                "file_size": file_size,
                "content_type": content_type,
                "success": success,
            },
        )

    @staticmethod
    def log_suspicious_activity(
        request,
        activity_type: str,
        reason: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log suspicious activity.

        Args:
            request: Django request object
            activity_type: Type of suspicious activity
            reason: Reason for flagging as suspicious
            data: Additional data
        """
        AuditLogManager.log_event(
            request,
            event_type="suspicious_activity",
            action=f"Suspicious activity detected: {activity_type}",
            severity="high",
            data={
                "activity_type": activity_type,
                "reason": reason,
                **(data or {}),
            },
        )

    @staticmethod
    def log_failed_auth(request, reason: str) -> None:
        """
        Log failed authentication attempt.

        Args:
            request: Django request object
            reason: Reason for authentication failure
        """
        AuditLogManager.log_event(
            request,
            event_type="failed_auth",
            action="Authentication failed",
            severity="medium",
            data={"reason": reason},
        )

    @staticmethod
    def get_recent_suspicious_activity(
        days: int = 7,
        limit: int = 100,
    ) -> list:
        """
        Get recent suspicious activity.

        Args:
            days: Number of days to look back
            limit: Maximum number of records

        Returns:
            List of AuditLog objects
        """
        from datetime import timedelta

        threshold = timezone.now() - timedelta(days=days)
        return AuditLog.objects.filter(
            severity__in=["high", "critical"], timestamp__gte=threshold
        ).order_by("-timestamp")[:limit]


# Structured logging configuration
def setup_audit_logger():
    """Configure audit logger with JSON formatting."""
    audit_logger = logging.getLogger("audit")

    # Create file handler
    from pythonjsonlogger import jsonlogger

    handler = logging.FileHandler("logs/audit.log")
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.INFO)

    return audit_logger
