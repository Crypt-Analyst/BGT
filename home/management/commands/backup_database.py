"""
Database backup management command.
"""

import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Backup database and important files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Remove backups older than 30 days",
        )
        parser.add_argument(
            "--restore",
            type=str,
            help="Restore database from backup file",
        )

    def handle(self, *args, **options):
        if options["restore"]:
            self.restore_backup(options["restore"])
        elif options["clean"]:
            self.clean_old_backups()
        else:
            self.backup_database()

    def backup_database(self):
        """Create database backup."""
        backup_dir = settings.BASE_DIR / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_name = settings.DATABASES["default"]["NAME"]

        if "postgresql" in settings.DATABASES["default"]["ENGINE"]:
            # PostgreSQL backup
            db_config = settings.DATABASES["default"]
            backup_file = backup_dir / f"backup_postgres_{timestamp}.sql"

            try:
                subprocess.run(
                    [
                        "pg_dump",
                        "--host",
                        db_config.get("HOST", "localhost"),
                        "--port",
                        str(db_config.get("PORT", 5432)),
                        "--username",
                        db_config.get("USER", ""),
                        "--file",
                        str(backup_file),
                        db_config.get("NAME", ""),
                    ],
                    check=True,
                    env={**os.environ, "PGPASSWORD": db_config.get("PASSWORD", "")},
                )

                self.stdout.write(
                    self.style.SUCCESS(f"PostgreSQL backup created: {backup_file}")
                )
            except subprocess.CalledProcessError as e:
                raise CommandError(f"PostgreSQL backup failed: {str(e)}")

        else:
            # SQLite backup
            backup_file = backup_dir / f"backup_sqlite_{timestamp}.db"
            try:
                shutil.copy2(db_name, backup_file)
                self.stdout.write(
                    self.style.SUCCESS(f"SQLite backup created: {backup_file}")
                )
            except IOError as e:
                raise CommandError(f"SQLite backup failed: {str(e)}")

        # Backup media files
        media_root = settings.MEDIA_ROOT
        if media_root.exists():
            media_backup = backup_dir / f"media_{timestamp}.tar.gz"
            try:
                subprocess.run(
                    [
                        "tar",
                        "-czf",
                        str(media_backup),
                        "-C",
                        str(media_root.parent),
                        media_root.name,
                    ],
                    check=True,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Media backup created: {media_backup}")
                )
            except subprocess.CalledProcessError as e:
                self.stdout.write(self.style.WARNING(f"Media backup failed: {str(e)}"))

    def restore_backup(self, backup_file):
        """Restore database from backup."""
        backup_path = Path(backup_file)

        if not backup_path.exists():
            raise CommandError(f"Backup file not found: {backup_file}")

        if backup_path.suffix == ".sql":
            # PostgreSQL restore
            db_config = settings.DATABASES["default"]
            try:
                with open(backup_path, "r") as f:
                    subprocess.run(
                        [
                            "psql",
                            "--host",
                            db_config.get("HOST", "localhost"),
                            "--port",
                            str(db_config.get("PORT", 5432)),
                            "--username",
                            db_config.get("USER", ""),
                            db_config.get("NAME", ""),
                        ],
                        stdin=f,
                        check=True,
                        env={**os.environ, "PGPASSWORD": db_config.get("PASSWORD", "")},
                    )

                self.stdout.write(
                    self.style.SUCCESS(f"Database restored from: {backup_file}")
                )
            except subprocess.CalledProcessError as e:
                raise CommandError(f"PostgreSQL restore failed: {str(e)}")

        elif backup_path.suffix == ".db":
            # SQLite restore
            db_name = settings.DATABASES["default"]["NAME"]
            try:
                shutil.copy2(backup_path, db_name)
                self.stdout.write(
                    self.style.SUCCESS(f"Database restored from: {backup_file}")
                )
            except IOError as e:
                raise CommandError(f"SQLite restore failed: {str(e)}")

    def clean_old_backups(self, days=30):
        """Remove backups older than specified days."""
        backup_dir = settings.BASE_DIR / "backups"

        if not backup_dir.exists():
            self.stdout.write(self.style.WARNING("Backup directory not found"))
            return

        cutoff_time = datetime.now() - timedelta(days=days)
        removed_count = 0

        for backup_file in backup_dir.glob("backup_*"):
            if backup_file.stat().st_mtime < cutoff_time.timestamp():
                try:
                    backup_file.unlink()
                    removed_count += 1
                except OSError as e:
                    self.stdout.write(
                        self.style.WARNING(f"Failed to remove {backup_file}: {str(e)}")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"Removed {removed_count} old backup files")
        )
