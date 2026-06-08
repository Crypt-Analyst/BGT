"""
Two-Factor Authentication models and utilities.
"""

import base64
from io import BytesIO

import pyotp
import qrcode
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserTwoFactorAuth(models.Model):
    """Model for storing user 2FA settings."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="two_factor_auth"
    )
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=32, blank=True)
    backup_codes = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_verified = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User Two-Factor Authentication"
        verbose_name_plural = "User Two-Factor Authentications"

    def __str__(self) -> str:
        return f"2FA for {self.user.username}"

    def generate_secret(self) -> str:
        """Generate a new TOTP secret."""
        self.secret_key = pyotp.random_base32()
        self.save()
        return self.secret_key

    def get_totp(self) -> pyotp.TOTP:
        """Get TOTP object for verification."""
        if not self.secret_key:
            raise ValueError("Secret key not set")
        return pyotp.TOTP(self.secret_key)

    def verify_token(self, token: str) -> bool:
        """
        Verify TOTP token.

        Args:
            token: 6-digit TOTP token

        Returns:
            True if token is valid
        """
        if not self.secret_key:
            return False

        totp = self.get_totp()
        # Allow 30 seconds of clock drift
        return totp.verify(token, valid_window=1)

    def generate_backup_codes(self, count: int = 10) -> list:
        """
        Generate backup codes for account recovery.

        Args:
            count: Number of backup codes to generate

        Returns:
            List of backup codes
        """
        import secrets

        codes = [secrets.token_hex(4).upper() for _ in range(count)]
        self.backup_codes = codes
        self.save()
        return codes

    def use_backup_code(self, code: str) -> bool:
        """
        Use and consume a backup code.

        Args:
            code: Backup code to use

        Returns:
            True if code was valid and consumed
        """
        if code in self.backup_codes:
            self.backup_codes.remove(code)
            self.save()
            return True
        return False

    def get_qr_code_image(self) -> str:
        """
        Generate QR code image for 2FA setup.

        Returns:
            Base64 encoded QR code image
        """
        if not self.secret_key:
            raise ValueError("Secret key not set")

        totp = self.get_totp()
        uri = totp.provisioning_uri(
            name=self.user.email, issuer_name="Bwire Global Tech"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_base64}"


class TwoFactorAuthenticationLog(models.Model):
    """Log for tracking 2FA events."""

    EVENT_TYPES = (
        ("enabled", "2FA Enabled"),
        ("disabled", "2FA Disabled"),
        ("token_verified", "Token Verified"),
        ("token_failed", "Token Verification Failed"),
        ("backup_code_used", "Backup Code Used"),
        ("qr_generated", "QR Code Generated"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="two_factor_logs"
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.event_type}"


class TwoFactorAuthManager:
    """Manager for 2FA operations."""

    @staticmethod
    def enable_2fa(user: User) -> tuple[str, list]:
        """
        Enable 2FA for user.

        Args:
            user: User to enable 2FA for

        Returns:
            Tuple of (secret_key, backup_codes)
        """
        tfa, created = UserTwoFactorAuth.objects.get_or_create(user=user)
        secret = tfa.generate_secret()
        backup_codes = tfa.generate_backup_codes()

        return secret, backup_codes

    @staticmethod
    def disable_2fa(user: User) -> None:
        """
        Disable 2FA for user.

        Args:
            user: User to disable 2FA for
        """
        try:
            tfa = user.two_factor_auth
            tfa.is_enabled = False
            tfa.secret_key = ""
            tfa.backup_codes = []
            tfa.save()
        except UserTwoFactorAuth.DoesNotExist:
            pass

    @staticmethod
    def verify_token(user: User, token: str) -> bool:
        """
        Verify 2FA token for user.

        Args:
            user: User to verify for
            token: Token to verify

        Returns:
            True if token is valid
        """
        try:
            tfa = user.two_factor_auth
            if not tfa.is_enabled:
                return False

            if tfa.verify_token(token):
                tfa.last_verified = timezone.now()
                tfa.save()
                return True

            # Try backup code
            if tfa.use_backup_code(token):
                return True

            return False
        except UserTwoFactorAuth.DoesNotExist:
            return False
