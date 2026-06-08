"""
Security monitoring management command.
"""

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings
from home.audit import AuditLog, AuditLogManager


class Command(BaseCommand):
    help = "Monitor security events and check for suspicious activity"

    def add_arguments(self, parser):
        parser.add_argument(
            "--report",
            action="store_true",
            help="Generate security report",
        )
        parser.add_argument(
            "--suspicious",
            action="store_true",
            help="List suspicious activities",
        )
        parser.add_argument(
            "--check-logins",
            action="store_true",
            help="Check for suspicious login attempts",
        )

    def handle(self, *args, **options):
        if options["report"]:
            self.generate_report()
        elif options["suspicious"]:
            self.list_suspicious()
        elif options["check_logins"]:
            self.check_login_attempts()
        else:
            self.generate_report()

    def generate_report(self):
        """Generate security report for last 7 days."""
        report_date = datetime.now().date()
        lookback_days = 7

        self.stdout.write(
            self.style.SUCCESS(f"=== Security Report ({report_date}) ===")
        )

        # Login events
        login_events = AuditLog.objects.filter(
            event_type="login",
            timestamp__gte=datetime.now() - timedelta(days=lookback_days),
        ).count()
        self.stdout.write(f"Successful Logins (7 days): {login_events}")

        # Failed login attempts
        failed_logins = AuditLog.objects.filter(
            event_type__in=["login_failed", "failed_auth"],
            timestamp__gte=datetime.now() - timedelta(days=lookback_days),
        ).count()
        self.stdout.write(
            self.style.WARNING(f"Failed Login Attempts (7 days): {failed_logins}")
        )

        # File uploads
        uploads = AuditLog.objects.filter(
            event_type="file_upload",
            timestamp__gte=datetime.now() - timedelta(days=lookback_days),
        ).count()
        self.stdout.write(f"File Uploads (7 days): {uploads}")

        # High severity events
        high_severity = AuditLog.objects.filter(
            severity__in=["high", "critical"],
            timestamp__gte=datetime.now() - timedelta(days=lookback_days),
        ).count()
        self.stdout.write(
            self.style.ERROR(f"High/Critical Events (7 days): {high_severity}")
        )

        # Top IP addresses by activity
        self.stdout.write("\n--- Top IP Addresses (Last 7 Days) ---")
        from django.db.models import Count

        top_ips = (
            AuditLog.objects.filter(
                timestamp__gte=datetime.now() - timedelta(days=lookback_days)
            )
            .values("ip_address")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        for entry in top_ips:
            self.stdout.write(f"{entry['ip_address']}: {entry['count']} events")

    def list_suspicious(self):
        """List suspicious activities."""
        suspicious = AuditLogManager.get_recent_suspicious_activity(days=7)

        self.stdout.write(
            self.style.ERROR(f"=== Suspicious Activities (Last 7 Days) ===")
        )

        if not suspicious.exists():
            self.stdout.write("No suspicious activities detected.")
            return

        for log in suspicious:
            self.stdout.write(f"\n[{log.severity.upper()}] {log.event_type}")
            self.stdout.write(f'  User: {log.user or "Anonymous"}')
            self.stdout.write(f"  IP: {log.ip_address}")
            self.stdout.write(f"  Action: {log.action}")
            self.stdout.write(f"  Time: {log.timestamp}")

    def check_login_attempts(self):
        """Check for suspicious login attempts."""
        one_hour_ago = datetime.now() - timedelta(hours=1)

        # Get failed login attempts in the last hour
        from django.db.models import Count

        failed_ips = (
            AuditLog.objects.filter(
                event_type__in=["login_failed", "failed_auth"],
                timestamp__gte=one_hour_ago,
            )
            .values("ip_address")
            .annotate(count=Count("id"))
            .filter(count__gte=5)
            .order_by("-count")
        )

        if not failed_ips.exists():
            self.stdout.write(
                self.style.SUCCESS("No suspicious login attempts detected.")
            )
            return

        self.stdout.write(
            self.style.WARNING("=== Suspicious Login Attempts (Last Hour) ===")
        )

        for entry in failed_ips:
            self.stdout.write(
                self.style.ERROR(
                    f"IP {entry['ip_address']}: {entry['count']} failed attempts"
                )
            )

            # Get details
            attempts = AuditLog.objects.filter(
                event_type__in=["login_failed", "failed_auth"],
                ip_address=entry["ip_address"],
                timestamp__gte=one_hour_ago,
            ).order_by("-timestamp")[:3]

            for attempt in attempts:
                self.stdout.write(
                    f"  - {attempt.timestamp}: {attempt.data.get('reason', 'Unknown')}"
                )
