## Performance Metrics & Testing

To measure page load, Lighthouse scores, and Core Web Vitals:

- Use Chrome DevTools > Lighthouse tab for audits (performance, accessibility, SEO, best practices).
- Use https://web.dev/measure/ for Core Web Vitals and lab data.
- Set `GOOGLE_ANALYTICS_MEASUREMENT_ID` in `.env` to enable real analytics and Web Vitals reporting.
- Optional `GOOGLE_OPTIMIZE_CONTAINER_ID` enables A/B experiment support.
- A GitHub Actions performance audit is available in `.github/workflows/performance-audit.yml`.
- The site now assigns an A/B test variant for the header CTA and tracks it through analytics.
# Bwire Global Tech

Starter Django site for Bwire Global Tech, styled around the brand colors from the supplied logo.

## Run locally

Create a `.env` file from `.env.example` or set environment variables directly.

```bash
python -m pip install -r requirements.txt
copy .env.example .env
# Windows PowerShell
python manage.py migrate
python manage.py seed_cms
python manage.py runsslserver 127.0.0.1:8000
```

If you prefer shell variables instead of `.env`, use:

```bash
setx OPENAI_API_KEY "your_api_key_here"
setx DJANGO_SECRET_KEY "change-me"
setx DJANGO_DEBUG "False"
setx DJANGO_ENABLE_SSL "False"
setx DJANGO_SECURE_SSL_REDIRECT "False"
setx DJANGO_ALLOWED_HOSTS "localhost,127.0.0.1"
setx DJANGO_CSRF_TRUSTED_ORIGINS "https://localhost:8000"
setx DJANGO_CORS_ALLOWED_ORIGINS "https://localhost:8000"
python manage.py migrate
python manage.py seed_cms
python manage.py runsslserver 127.0.0.1:8000
```

The homepage is at `https://127.0.0.1:8000/`.

If you also run a separate frontend dev server at `https://localhost:5173`, the backend is configured to allow secure local cross-origin requests.

For HTTPS locally, run:

```bash
python manage.py runsslserver 127.0.0.1:8000
```

Then open:

```text
https://127.0.0.1:8000/
```

If port `8000` is already in use by the HTTP dev server, run HTTPS on a different port:

```bash
python manage.py runsslserver 127.0.0.1:8443
```

Then open:

```text
https://127.0.0.1:8443/
```

If you want both HTTP and HTTPS at the same time, run the two servers in separate terminals.

## Security notes

- A basic Content Security Policy and security headers are enabled.
- The chat endpoint is rate-limited to 12 requests per minute per IP.
- Uploads are capped at ~2.5MB per request.

## Render deployment

This project is ready to deploy on Render using the existing `Dockerfile`.

- `requirements.txt` already includes the production dependencies needed for Render:
  - `gunicorn`
  - `psycopg[binary]`
  - `redis`
  - `django-redis`
  - `celery[redis]`
  - `whitenoise`
  - `django-cors-headers`

A `render.yaml` manifest has been added to define the web and worker services.

### Render environment variables

Set these in Render:

- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `DJANGO_EMAIL_HOST_PASSWORD`
- `OPENAI_API_KEY`
- `SENTRY_DSN` (optional)
- `DJANGO_ENABLE_SSL=True`
- `DJANGO_SECURE_PROXY_SSL_HEADER=True`

### Important note

The current app stores media files in local `MEDIA_ROOT`, which is not persistent on Render. For uploaded files to survive restarts, you should configure an external storage backend such as Amazon S3.
