import logging
import os
from typing import Any, Callable

from django.conf import settings
from django.core.mail import EmailMessage
from openai import OpenAI

logger = logging.getLogger("home.tasks")


# Provide a safe decorator that uses celery.shared_task when available,
# otherwise returns a no-op decorator that leaves the function callable.
try:
    from celery import shared_task as _shared_task  # type: ignore

    has_celery = True
except Exception:
    has_celery = False


def _task_decorator(*dargs: Any, **dkwargs: Any) -> Callable[[Callable], Callable]:
    if has_celery:
        return _shared_task(*dargs, **dkwargs)  # type: ignore

    def _noop_decorator(func: Callable) -> Callable:
        return func

    return _noop_decorator


@_task_decorator(ignore_result=True)
def send_email_task(
    subject: str,
    body: str,
    from_email: str,
    to_list: list,
    reply_to: list | None = None,
):
    """Send an email. When Celery is available this is a task; otherwise a normal function."""
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_list,
            reply_to=reply_to or [],
        )
        email.send(fail_silently=False)
        logger.info("send_email_task sent to %s subject=%s", to_list, subject)
    except Exception as exc:
        logger.exception("send_email_task failed: %s", exc)


@_task_decorator(ignore_result=True)
def call_openai_chat(
    messages: list, model: str = "gpt-4o-mini", temperature: float = 0.3
) -> dict:
    api_key = getattr(settings, "OPENAI_API_KEY", None) or os.environ.get(
        "OPENAI_API_KEY"
    )
    if not api_key:
        logger.error("Missing OPENAI_API_KEY")
        return {"ok": False, "error": "Missing OPENAI_API_KEY"}
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
        return {"ok": True, "response": response}
    except Exception as exc:
        logger.exception("call_openai_chat failed: %s", exc)
        return {"ok": False, "error": str(exc)}
