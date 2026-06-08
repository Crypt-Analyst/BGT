import json
import os
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ProjectRequest, SiteSettings


class HomeViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        SiteSettings.objects.create(
            site_name="Bwire Global Tech",
            tagline="The Mind Behind the Machine",
            owner_name="Bilford Derick Bwire",
            email="bwireglobaltech917@gmail.com",
            phone="0722206805",
            instagram="bwireglobaltech",
            tiktok="bwireglobaltech",
            whatsapp_number="254722206805",
            whatsapp_message="Hi Bwire Global Tech, I'd like to start a project.",
            footer_blurb="Premium digital systems with a strong visual identity, built for trust, speed, and conversion.",
            header_cta_label="Start a project",
        )

    def test_homepage_renders(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bwire Global Tech")

    def test_contact_get_renders(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Start a project")

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="no-reply@bwireglobaltech.com",
        CONTACT_EMAIL="contact@bwireglobaltech.com",
    )
    def test_contact_post_creates_project_request_and_sends_email(self):
        form_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "+254700000000",
            "project_type": "starter",
            "message": "I need a website.",
            "budget_range": "under-30000",
            "timeline": "2 weeks",
            "referral_source": "google",
        }

        response = self.client.post(reverse("contact"), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ProjectRequest.objects.filter(full_name="Test User").exists())
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("New project request", mail.outbox[0].subject)
        self.assertIn("We received your project request", mail.outbox[1].subject)

    def test_chat_ai_requires_api_key(self):
        response = self.client.post(
            reverse("chat_ai"),
            json.dumps({"message": "Hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["error"], "Missing OPENAI_API_KEY.")

    @patch("home.views.OpenAI")
    def test_chat_ai_returns_openai_response(self, mock_openai_class):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            client_instance = MagicMock()
            client_instance.chat.completions.create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="Hi there!"))]
            )
            mock_openai_class.return_value = client_instance

            response = self.client.post(
                reverse("chat_ai"),
                json.dumps({"message": "Hello"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["answer"], "Hi there!")
        mock_openai_class.assert_called_once_with(api_key="test-key")
