"""
Management command to generate encryption keys and initialize security settings.
"""
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = 'Generate security keys and initialize security configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--generate-encryption-key',
            action='store_true',
            help='Generate new encryption key',
        )
        parser.add_argument(
            '--django-secret-key',
            action='store_true',
            help='Generate new Django secret key',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generate all keys',
        )

    def handle(self, *args, **options):
        if options['all']:
            self.generate_encryption_key()
            self.generate_django_secret()
        elif options['generate_encryption_key']:
            self.generate_encryption_key()
        elif options['django_secret_key']:
            self.generate_django_secret()
        else:
            self.generate_encryption_key()
            self.generate_django_secret()

    def generate_encryption_key(self):
        """Generate and display encryption key."""
        from home.security import generate_encryption_key

        key = generate_encryption_key()
        self.stdout.write(
            self.style.SUCCESS('Generated Encryption Key:')
        )
        self.stdout.write(key)
        self.stdout.write(
            self.style.WARNING('\nAdd this to your .env file as:')
        )
        self.stdout.write(f'ENCRYPTION_KEY={key}')

    def generate_django_secret(self):
        """Generate and display Django secret key."""
        from django.core.management.utils import get_random_secret_key

        key = get_random_secret_key()
        self.stdout.write(
            self.style.SUCCESS('\nGenerated Django Secret Key:')
        )
        self.stdout.write(key)
        self.stdout.write(
            self.style.WARNING('\nAdd this to your .env file as:')
        )
        self.stdout.write(f'DJANGO_SECRET_KEY={key}')
