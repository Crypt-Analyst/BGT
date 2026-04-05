# Bwire Global Tech

Starter Django site for Bwire Global Tech, styled around the brand colors from the supplied logo.

## Run locally

```bash
python -m pip install -r requirements.txt
setx OPENAI_API_KEY "your_api_key_here"
setx DJANGO_SECRET_KEY "change-me"
setx DJANGO_DEBUG "False"
setx DJANGO_ALLOWED_HOSTS "yourdomain.com,www.yourdomain.com"
setx DJANGO_CSRF_TRUSTED_ORIGINS "https://yourdomain.com,https://www.yourdomain.com"
python manage.py runserver
```

The homepage is at `http://127.0.0.1:8000/`.

## Security notes

- A basic Content Security Policy and security headers are enabled.
- The chat endpoint is rate-limited to 12 requests per minute per IP.
- Uploads are capped at ~2.5MB per request.
