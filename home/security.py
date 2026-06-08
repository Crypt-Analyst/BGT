"""
Security utilities for encryption, data protection, and secure operations.
"""

import hashlib
import json
import logging
from typing import Any, Optional

import bleach
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(__name__)

# HTML tags allowed in sanitized output
ALLOWED_HTML_TAGS = {
    "p",
    "br",
    "strong",
    "em",
    "u",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "a",
    "blockquote",
    "code",
    "pre",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
}

ALLOWED_HTML_ATTRIBUTES = {
    "*": ["class", "id"],
    "a": ["href", "title", "target"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
}


class EncryptionManager:
    """Manage encryption and decryption of sensitive data."""

    def __init__(self):
        """Initialize encryption manager with key from settings."""
        encryption_key = getattr(settings, "ENCRYPTION_KEY", None)
        if not encryption_key:
            raise RuntimeError(
                "ENCRYPTION_KEY must be set in settings for data encryption"
            )
        self.cipher = Fernet(
            encryption_key.encode()
            if isinstance(encryption_key, str)
            else encryption_key
        )

    def encrypt(self, data: Any) -> str:
        """
        Encrypt data to string.

        Args:
            data: Data to encrypt (will be JSON-serialized)

        Returns:
            Encrypted string
        """
        try:
            json_data = json.dumps(data)
            encrypted = self.cipher.encrypt(json_data.encode())
            return encrypted.decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt(self, encrypted_data: str) -> Any:
        """
        Decrypt data from string.

        Args:
            encrypted_data: Encrypted string

        Returns:
            Decrypted data
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return json.loads(decrypted.decode())
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise


class InputValidator:
    """Validate and sanitize user input."""

    @staticmethod
    def sanitize_html(content: str) -> str:
        """
        Sanitize HTML content to prevent XSS.

        Args:
            content: HTML content to sanitize

        Returns:
            Sanitized HTML
        """
        if not content:
            return ""
        return bleach.clean(
            content,
            tags=ALLOWED_HTML_TAGS,
            attributes=ALLOWED_HTML_ATTRIBUTES,
            strip=True,
        )

    @staticmethod
    def sanitize_text(content: str) -> str:
        """
        Sanitize plain text by removing potentially dangerous characters.

        Args:
            content: Text to sanitize

        Returns:
            Sanitized text
        """
        if not content:
            return ""
        # Remove null bytes and other control characters
        return "".join(char for char in content if ord(char) >= 32 or char in "\n\r\t")

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format (basic check).

        Args:
            email: Email address to validate

        Returns:
            True if valid format, False otherwise
        """
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate phone number format.

        Args:
            phone: Phone number to validate

        Returns:
            True if valid format, False otherwise
        """
        import re

        # Allow various phone formats with country codes
        pattern = r"^\+?1?\d{9,15}$"
        return re.match(pattern, phone.replace(" ", "").replace("-", "")) is not None

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid format, False otherwise
        """
        import re

        pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        return re.match(pattern, url, re.IGNORECASE) is not None


class FileUploadValidator:
    """Validate file uploads for security."""

    # Allowed MIME types
    ALLOWED_MIMES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    # Dangerous file extensions
    DANGEROUS_EXTENSIONS = {
        "exe",
        "bat",
        "cmd",
        "com",
        "pif",
        "scr",
        "vbs",
        "js",
        "jar",
        "zip",
        "rar",
        "7z",
        "iso",
        "dmg",
        "app",
        "sh",
        "py",
        "php",
        "asp",
        "jsp",
        "pl",
        "rb",
        "cgi",
    }

    # Maximum file sizes by type (in bytes)
    MAX_SIZES = {
        "image": 5 * 1024 * 1024,  # 5MB
        "pdf": 10 * 1024 * 1024,  # 10MB
        "document": 10 * 1024 * 1024,  # 10MB
    }

    @staticmethod
    def validate_file(file_obj, max_size: Optional[int] = None) -> tuple[bool, str]:
        """
        Validate uploaded file.

        Args:
            file_obj: Django UploadedFile object
            max_size: Maximum file size in bytes

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_obj:
            return False, "No file provided"

        # Check file extension
        filename = file_obj.name.lower()
        file_extension = filename.split(".")[-1] if "." in filename else ""

        if file_extension in FileUploadValidator.DANGEROUS_EXTENSIONS:
            return False, f"File type '.{file_extension}' is not allowed"

        # Check file size
        if file_obj.size == 0:
            return False, "File is empty"

        if max_size and file_obj.size > max_size:
            return False, f"File exceeds maximum size of {max_size / 1024 / 1024:.1f}MB"

        # Check MIME type
        mime_type = file_obj.content_type
        if mime_type not in FileUploadValidator.ALLOWED_MIMES:
            return False, f"File type '{mime_type}' is not allowed"

        return True, ""

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize uploaded filename.

        Args:
            filename: Original filename

        Returns:
            Safe filename
        """
        # Remove path separators and dangerous characters
        filename = filename.replace("\\", "").replace("/", "")
        # Create safe slug
        name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        safe_name = slugify(name)
        # Add timestamp to prevent collisions
        timestamp = hashlib.md5(filename.encode()).hexdigest()[:8]
        return f"{safe_name}_{timestamp}.{ext}" if ext else f"{safe_name}_{timestamp}"


class PasswordValidator:
    """Validate password strength."""

    @staticmethod
    def validate_strength(password: str) -> tuple[bool, list[str]]:
        """
        Validate password strength requirements.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if len(password) < 12:
            errors.append("Password must be at least 12 characters long")

        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            errors.append("Password must contain at least one lowercase letter")

        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit")

        if not any(char in "!@#$%^&*()-_+={}[]|:;<>?,./~`" for char in password):
            errors.append("Password must contain at least one special character")

        return len(errors) == 0, errors


def generate_encryption_key():
    """Generate a new encryption key."""
    return Fernet.generate_key().decode()
