"""Management command to check production readiness."""

from django.conf import settings
from django.core.management.base import BaseCommand

from bwire_global_tech.production import (
    check_production_ready,
    get_production_checklist,
)


class Command(BaseCommand):
    help = "Check if the application is ready for production deployment"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n=== Production Readiness Check ===\n"))

        checks = check_production_ready()

        # Status
        status_style = (
            self.style.SUCCESS
            if checks["status"] == "ready"
            else (
                self.style.WARNING
                if checks["status"] == "ready_with_warnings"
                else self.style.ERROR
            )
        )
        self.stdout.write(status_style(f"Status: {checks['status'].upper()}"))

        # Errors
        if checks["errors"]:
            self.stdout.write(self.style.ERROR("\nErrors (must fix):"))
            for error in checks["errors"]:
                self.stdout.write(f"  ✗ {error}")

        # Warnings
        if checks["warnings"]:
            self.stdout.write(self.style.WARNING("\nWarnings (should fix):"))
            for warning in checks["warnings"]:
                self.stdout.write(f"  ⚠ {warning}")

        if not checks["errors"] and not checks["warnings"]:
            self.stdout.write(self.style.SUCCESS("\nNo issues found!"))

        # Show checklist
        self.stdout.write(self.style.SUCCESS("\n=== Deployment Checklist ===\n"))
        checklist = get_production_checklist()

        for section, items in checklist.items():
            self.stdout.write(
                self.style.HTTP_INFO(f"\n{section.upper().replace('_', ' ')}:")
            )
            for i, item in enumerate(items, 1):
                self.stdout.write(f"  [ ] {i}. {item}")

        self.stdout.write("\n")
