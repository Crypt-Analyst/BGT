import logging
from urllib.parse import quote

from django.conf import settings
from django.core.mail import EmailMessage

from .models import ProjectRequest, SiteSettings

logger = logging.getLogger("home.services")

SITE_NAME = "Bwire Global Tech"
TAGLINE = "The Mind Behind the Machine"
SITE_CONTEXT = """
Site name: Bwire Global Tech
Tagline: The Mind Behind the Machine
Positioning: Web development first. AI second.

Home: We build websites first, then AI solutions that support the business. Focus on real work, not generic filler.
Highlights: Web development, AI solutions, dashboards and support. CTA: Start a project, See the vision.

About: Mission is to build practical websites that help businesses show up professionally online.
Vision is to be a trusted partner for modern web development and useful AI work.
Owner: Bilford Derick Bwire.

Services: Software development for landing pages, business portals, and internal tools.
AI solutions include assistants, predictive models, BwiResQ AI ideas, and smart analytics.
Support services include cloud setup, security checks, maintenance plans.
Design and dashboards include graphic design, UI support, reporting dashboards.
Delivery flow: Discover goals and AI needs, Design pages and conversion path, Launch and refine content and performance.

Portfolio: Case studies include corporate rebrand website, AI services landing page, business systems hub.
Outcomes: +42% longer engagement, +31% more inquiries, 100% brand consistency.
Deep dive: Corporate rebrand website improved engagement and inquiries with a new story and consistent visual system.

Testimonials: Premium web presence, faster delivery, clearer messaging, and stronger conversion flow.

Pricing page: Web development packages, AI price, add-ons, and payment notes.
Deliverables: Production-ready site, performance baseline, growth roadmap.
Packages: Starter (Ksh 30,000), Business (Ksh 65,000), Premium (Ksh 120,000).
AI solutions: $700 per project.
Add-ons: domain registration, hosting, maintenance, SEO package, extra pages.
Notes: 50% deposit before start, balance after completion, prices may vary by requirements.

Contact: Email bwireglobaltech917@gmail.com, phone 0722206805.
Contact page requests: business name, website goals, AI idea if needed, deadline or launch date.
Next steps: Review, call, proposal.
""".strip()


def get_site_settings():
    return SiteSettings.objects.first()


def build_whatsapp_link(site_settings: SiteSettings | None) -> str:
    number = site_settings.whatsapp_number if site_settings else "254722206805"
    message = (
        site_settings.whatsapp_message
        if site_settings
        else "Hi Bwire Global Tech, I'd like to start a project."
    )
    return f"https://wa.me/{number}?text={quote(message)}"


def site_context(page_title: str, page_description: str, active_page: str) -> dict:
    site_settings = get_site_settings()
    return {
        "site_settings": site_settings,
        "site_name": site_settings.site_name if site_settings else SITE_NAME,
        "tagline": site_settings.tagline if site_settings else TAGLINE,
        "page_title": page_title,
        "page_description": page_description,
        "active_page": active_page,
        "whatsapp_link": build_whatsapp_link(site_settings),
        "google_analytics_id": settings.GOOGLE_ANALYTICS_MEASUREMENT_ID,
        "google_optimize_id": settings.GOOGLE_OPTIMIZE_CONTAINER_ID,
        "nav_items": [
            {"label": "Home", "url_name": "home", "name": "home"},
            {"label": "About", "url_name": "about", "name": "about"},
            {"label": "Services", "url_name": "services", "name": "services"},
            {"label": "Pricing", "url_name": "pricing", "name": "pricing"},
            {"label": "Portfolio", "url_name": "portfolio", "name": "portfolio"},
            {"label": "Gallery", "url_name": "gallery", "name": "gallery"},
            {"label": "Contact", "url_name": "contact", "name": "contact"},
        ],
    }


def create_project_request(cleaned_data: dict):
    return ProjectRequest.objects.create(
        full_name=cleaned_data["full_name"],
        email=cleaned_data["email"],
        phone=cleaned_data["phone"],
        project_type=cleaned_data["project_type"],
        message=cleaned_data["message"],
        budget_range=cleaned_data.get("budget_range", ""),
        timeline=cleaned_data.get("timeline", ""),
        referral_source=cleaned_data.get("referral_source", ""),
        reference_file=cleaned_data.get("reference_file"),
    )


def build_contact_emails(cleaned_data: dict, user_email: str):
    admin_subject = f"New project request: {cleaned_data['full_name']}"
    admin_body = (
        f"Full name: {cleaned_data['full_name']}\n"
        f"Email: {cleaned_data['email']}\n"
        f"Phone: {cleaned_data['phone']}\n"
        f"Project type: {cleaned_data['project_type']}\n"
        f"Budget range: {cleaned_data.get('budget_range') or 'Not provided'}\n"
        f"Timeline: {cleaned_data.get('timeline') or 'Not provided'}\n"
        f"Referral source: {cleaned_data.get('referral_source') or 'Not provided'}\n\n"
        "Project description:\n"
        f"{cleaned_data['message']}\n"
    )
    visitor_subject = "We received your project request"
    visitor_body = (
        "Thanks for reaching out to Bwire Global Tech.\n\n"
        "We have received your project request and will get back to you within 24 hours.\n"
        "If you need to add more details, just reply to this email."
    )
    admin_email = EmailMessage(
        subject=admin_subject,
        body=admin_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_EMAIL],
        reply_to=[user_email],
    )
    visitor_email = EmailMessage(
        subject=visitor_subject,
        body=visitor_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    return admin_email, visitor_email


def build_chat_messages(user_message: str, history: list) -> list:
    messages = [
        {
            "role": "system",
            "content": (
                "You are Lee, the assistant for the Bwire Global Tech website. "
                "Use ONLY the site context provided. "
                "First, make sure you understand the visitor's request; if it is vague, ask a short "
                "clarifying question. "
                "Avoid generic filler and keep responses concise and specific to Bwire Global Tech. "
                "If the answer is not in the context, say you do not know and ask the visitor "
                "to contact the team via email or phone."
            ),
        },
        {"role": "system", "content": f"Site context:\n{SITE_CONTEXT}"},
    ]
    for item in history[-8:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": user_message})
    return messages
