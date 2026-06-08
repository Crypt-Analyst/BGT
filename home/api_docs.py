"""API documentation endpoint."""

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_docs(request):
    """API documentation endpoint."""
    docs = {
        "title": "Bwire Global Tech API",
        "version": "1.0.0",
        "endpoints": {
            "chat": {
                "url": reverse("chat_ai"),
                "method": "POST",
                "description": "Chat with Lee, the AI assistant",
                "content_type": "application/json",
                "rate_limit": "12 requests per minute per IP",
                "request_body": {
                    "message": "string (required) - User message",
                    "history": "array (optional) - Conversation history with role/content pairs",
                },
                "response": {
                    "answer": "string - AI response",
                },
                "error_responses": {
                    "400": "Invalid JSON or missing message",
                    "500": "Missing OPENAI_API_KEY",
                    "503": "AI service unavailable",
                },
                "example_request": {
                    "message": "What services does Bwire Global Tech offer?",
                    "history": [],
                },
                "example_response": {
                    "answer": "Bwire Global Tech offers web development, AI solutions, and support services.",
                },
            },
            "contact": {
                "url": reverse("contact"),
                "method": "POST",
                "description": "Submit a project contact request",
                "content_type": "application/x-www-form-urlencoded",
                "request_fields": {
                    "full_name": "string (required)",
                    "email": "string (required)",
                    "phone": "string (required)",
                    "project_type": "string (required) - starter, business, premium, ai_solution",
                    "message": "string (required)",
                    "budget_range": "string (optional)",
                    "timeline": "string (optional)",
                    "referral_source": "string (optional)",
                    "reference_file": "file (optional)",
                },
                "response": "Contact form page with success message",
            },
        },
    }
    return JsonResponse(docs)
