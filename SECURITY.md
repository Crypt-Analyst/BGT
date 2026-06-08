# Security Configuration Guide

## Overview
This document outlines all security measures implemented for the Bwire Global Tech platform.

## 1. HTTPS/SSL Certificates

### Configuration
```env
DJANGO_ENABLE_SSL=True
DJANGO_SECURE_SSL_REDIRECT=True
```

### Setup Instructions

**For Development:**
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run development server with SSL
python manage.py runsslserver 0.0.0.0:8000 --certificate cert.pem --key key.pem
```

**For Production:**
1. Use Let's Encrypt with Certbot:
```bash
certbot certonly --standalone -d yourdomain.com
```

2. Configure Nginx:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
}
```

3. Auto-renewal:
```bash
certbot renew --dry-run
```

### HSTS Settings
- Enabled with 2-year max age
- Includes subdomains
- HSTS preload enabled
- Redirects all HTTP to HTTPS

---

## 2. CSRF Protection

### Enabled Features
- Django CSRF middleware active
- CSRF tokens required on all forms
- Secure cookie transmission
- CORS validation

### Configuration
```python
CSRF_COOKIE_SECURE = True  # HTTPS only
CSRF_COOKIE_HTTPONLY = True  # No JS access
CSRF_COOKIE_SAMESITE = 'Lax'  # Cross-site restrictions
CSRF_TRUSTED_ORIGINS = [...]  # Whitelist of safe origins
```

### Frontend Implementation
```html
<!-- Include CSRF token in forms -->
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

## 3. XSS Protection

### Implemented Measures
1. **Content Security Policy (CSP)**
   - Restricts script sources
   - Disables inline scripts
   - Blocks unsafe content

2. **HTML Sanitization**
   - User input is sanitized using `bleach` library
   - Allowed tags: p, br, strong, em, ul, ol, li, a, code, etc.
   - Dangerous attributes stripped

3. **Template Auto-escaping**
   - Django template engine escapes by default
   - Use `{{ variable }}` for safe escaping

4. **Security Headers**
   ```
   X-Content-Type-Options: nosniff
   X-Frame-Options: DENY
   X-XSS-Protection: 1; mode=block
   ```

### Usage
```python
from home.security import InputValidator

# Sanitize HTML input
clean_html = InputValidator.sanitize_html(user_input)

# Sanitize text
clean_text = InputValidator.sanitize_text(user_input)
```

---

## 4. SQL Injection Prevention

### Built-in Protection
- Django ORM parameterized queries prevent SQL injection
- Never use raw SQL with string concatenation

### Safe Example
```python
# ✓ SAFE - Using ORM
from home.models import ProjectRequest
projects = ProjectRequest.objects.filter(email=user_email)

# ✗ UNSAFE - Raw SQL
from django.db import connection
cursor = connection.cursor()
cursor.execute(f"SELECT * FROM home_projectrequest WHERE email = '{user_email}'")
```

### Additional Protection
- SQL Injection Protection Middleware monitors suspicious patterns
- Detects: DROP, DELETE, UNION SELECT, OR 1=1, EXEC

---

## 5. Input Validation

### Validators Available
```python
from home.security import InputValidator

# Email validation
if InputValidator.validate_email(email):
    # process email

# Phone validation  
if InputValidator.validate_phone(phone):
    # process phone

# URL validation
if InputValidator.validate_url(url):
    # process URL
```

### Form Validation
```python
from django import forms
from django.core.exceptions import ValidationError

class ProjectRequestForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data['email']
        if ProjectRequest.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered")
        return email
```

---

## 6. Rate Limiting

### Configuration
```env
CHAT_RATE_LIMIT_MAX_REQUESTS=12
CHAT_RATE_LIMIT_WINDOW_SECONDS=60
API_RATE_LIMIT_REQUESTS=1000
API_RATE_LIMIT_PERIOD=3600
```

### Endpoints Protected
- `/api/chat/` - 12 requests per minute
- All API endpoints - 1000 requests per hour

### Custom Rate Limiting
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/h')
def sensitive_view(request):
    # View code
    pass
```

---

## 7. Session Security

### Configuration
```python
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JS access
SESSION_COOKIE_SAMESITE = 'Lax'  # Cross-site restrictions
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 604800  # 7 days
```

### Secure Session Handling
```python
# Regenerate session after login
from django.contrib.auth import login

def login_view(request):
    user = authenticate(username=username, password=password)
    if user:
        request.session.flush()  # Prevent session fixation
        login(request, user)
```

---

## 8. Secure File Uploads

### Validation
```python
from home.security import FileUploadValidator

# Validate file
is_valid, error = FileUploadValidator.validate_file(uploaded_file, max_size=5*1024*1024)

if not is_valid:
    # Handle error
    pass

# Sanitize filename
safe_name = FileUploadValidator.sanitize_filename(original_filename)
```

### Allowed File Types
- Images: JPEG, PNG, WebP
- Documents: PDF, Word, Excel

### Restrictions
- Maximum size: 5MB (configurable)
- Dangerous extensions blocked: .exe, .bat, .py, .sh, etc.
- MIME type verification
- Filename sanitization

---

## 9. Data Encryption

### Setup
```python
# Generate new encryption key
from home.security import generate_encryption_key
key = generate_encryption_key()
# Add to .env: ENCRYPTION_KEY=<generated_key>
```

### Usage
```python
from home.security import EncryptionManager

manager = EncryptionManager()

# Encrypt sensitive data
encrypted = manager.encrypt({"credit_card": "1234-5678-9012-3456"})

# Decrypt data
decrypted = manager.decrypt(encrypted)
```

### Encrypted Fields in Models
```python
from django.db import models

class SensitiveData(models.Model):
    encrypted_info = models.TextField()
    
    def save(self, *args, **kwargs):
        manager = EncryptionManager()
        self.encrypted_info = manager.encrypt(self.sensitive_data)
        super().save(*args, **kwargs)
```

---

## 10. Backups & Recovery

### Automated Backups
```bash
# Daily backup (add to crontab)
0 2 * * * cd /path/to/project && python manage.py backup_database

# Weekly backup cleanup
0 3 * * 0 cd /path/to/project && python manage.py backup_database --clean
```

### Manual Backup
```bash
# Create backup
python manage.py backup_database

# Backup files stored in: backups/
```

### Restoration
```bash
# Restore from backup
python manage.py backup_database --restore /path/to/backup_file.sql
```

---

## 11. Audit Logging

### Logged Events
- User logins and logouts
- Failed authentication attempts
- Password changes
- File uploads/downloads
- Data access and modifications
- Admin actions
- Security alerts

### Viewing Audit Logs
```python
from home.audit import AuditLog

# Get recent logs
logs = AuditLog.objects.filter(
    user=request.user
).order_by('-timestamp')[:100]

# Get suspicious activity
high_severity = AuditLog.objects.filter(
    severity__in=['high', 'critical']
)

# Export logs
from django.core import management
management.call_command('dumpdata', 'home.AuditLog', indent=2)
```

### Log Locations
- Application logs: `logs/app.log`
- Audit logs: `logs/audit.log`
- Security logs: `logs/security.log`

---

## 12. Two-Factor Authentication (2FA)

### Enable for User
```python
from home.two_factor_auth import TwoFactorAuthManager

# Enable 2FA
secret, backup_codes = TwoFactorAuthManager.enable_2fa(user)

# Get QR code for authenticator app
qr_code_image = user.two_factor_auth.get_qr_code_image()
```

### Verify Token
```python
# Verify TOTP token
if TwoFactorAuthManager.verify_token(user, user_token):
    # Token valid, proceed with login
    pass
```

### Backup Codes
```python
# Generate new backup codes
backup_codes = user.two_factor_auth.generate_backup_codes()

# Use backup code
if user.two_factor_auth.use_backup_code(code):
    # Backup code consumed, user authenticated
    pass
```

### Implementation in Login Flow
```python
def login_view(request):
    # Standard authentication
    user = authenticate(username, password)
    
    if user:
        # Check if 2FA enabled
        if hasattr(user, 'two_factor_auth') and user.two_factor_auth.is_enabled:
            # Redirect to 2FA verification
            request.session['user_id'] = user.id
            return redirect('verify_2fa')
        
        # No 2FA, login normally
        login(request, user)
        return redirect('home')
```

---

## 13. Security Monitoring

### Automated Checks
```bash
# Generate security report
python manage.py security_monitor --report

# Check for suspicious activities
python manage.py security_monitor --suspicious

# Check login attempts
python manage.py security_monitor --check-logins
```

### Sentry Integration
```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

Sentry automatically tracks:
- Unhandled exceptions
- Performance issues
- Error rates
- User interactions

### Monitoring Endpoints
Access audit logs in Django admin:
```
/admin/home/auditlog/
```

---

## Environment Configuration

### Development (.env)
```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_ENABLE_SSL=False
ENCRYPTION_KEY=generated-encryption-key
```

### Production (.env)
```env
DJANGO_SECRET_KEY=strong-random-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_ENABLE_SSL=True
DJANGO_SECURE_SSL_REDIRECT=True
ENCRYPTION_KEY=generated-encryption-key
DATABASE_URL=postgresql://user:password@host:port/dbname
SENTRY_DSN=your-sentry-dsn
```

---

## Security Checklist

- [ ] SSL/HTTPS configured and certificates valid
- [ ] CSRF tokens enabled on all forms
- [ ] CSP headers configured
- [ ] Input validation on all forms
- [ ] File upload restrictions in place
- [ ] Rate limiting enabled
- [ ] Audit logging operational
- [ ] Database backups scheduled
- [ ] 2FA option available
- [ ] Security monitoring (Sentry) active
- [ ] Regular security audits scheduled
- [ ] Dependencies updated regularly
- [ ] Staff trained on security practices
- [ ] Incident response plan documented

---

## Additional Resources

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Sentry Docs](https://docs.sentry.io/)
