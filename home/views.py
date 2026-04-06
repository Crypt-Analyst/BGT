import json
import os
from urllib.parse import quote

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from openai import OpenAI

from .forms import ContactForm
from .models import (
    AboutCapability,
    AboutCard,
    AboutHero,
    AboutOwner,
    AboutStep,
    ContactChecklistItem,
    ContactHero,
    ContactNextStep,
    DeliverableItem,
    HomeCaseStudy,
    HomeCta,
    HomeFaq,
    HomeHero,
    HomeMetric,
    HomeService,
    HomeTestimonial,
    PortfolioDeepDive,
    PortfolioDeepDiveMetric,
    PortfolioHero,
    PortfolioItem,
    PortfolioOutcome,
    PrivacyPage,
    PricingAddon,
    PricingCta,
    PricingHero,
    PricingPackage,
    PricingTerms,
    ProjectRequest,
    ServiceItem,
    ServicesFaq,
    ServicesHero,
    SiteSettings,
    TermsPage,
    TimelineStep,
)


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
FAQ: Maintenance available, redesigns available, timelines set after brief review.

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
        "nav_items": [
            {"label": "Home", "url_name": "home", "name": "home"},
            {"label": "About", "url_name": "about", "name": "about"},
            {"label": "Services", "url_name": "services", "name": "services"},
            {"label": "Pricing", "url_name": "pricing", "name": "pricing"},
            {"label": "Portfolio", "url_name": "portfolio", "name": "portfolio"},
            {"label": "Contact", "url_name": "contact", "name": "contact"},
        ],
    }


def home(request):
    context = site_context(
        "Bwire Global Tech | The Mind Behind the Machine",
        "Bwire Global Tech builds premium websites, AI experiences, and digital systems inspired by the brand logo.",
        "home",
    )
    context.update(
        {
            "home_hero": HomeHero.objects.first(),
            "home_metrics": HomeMetric.objects.all(),
            "home_services": HomeService.objects.all(),
            "home_case_studies": HomeCaseStudy.objects.all(),
            "home_testimonials": HomeTestimonial.objects.all(),
            "home_faqs": HomeFaq.objects.all(),
            "home_cta": HomeCta.objects.first(),
        }
    )
    return render(request, "home/index.html", context)


def about(request):
    context = site_context(
        "About | Bwire Global Tech",
        "Learn the story, mission, and design direction behind Bwire Global Tech.",
        "about",
    )
    about_cards = AboutCard.objects.all()
    context.update(
        {
            "about_hero": AboutHero.objects.first(),
            "about_mission_vision": about_cards.filter(section__in=["mission", "vision"]),
            "about_what": about_cards.filter(section="what"),
            "about_values": about_cards.filter(section="values"),
            "about_steps": AboutStep.objects.all(),
            "about_capabilities": AboutCapability.objects.all(),
            "about_owner": AboutOwner.objects.first(),
        }
    )
    return render(request, "home/about.html", context)


def services(request):
    context = site_context(
        "Services | Bwire Global Tech",
        "Discover the services, systems, and delivery process behind the brand.",
        "services",
    )
    context.update(
        {
            "services_hero": ServicesHero.objects.first(),
            "service_items": ServiceItem.objects.all(),
            "deliverables": DeliverableItem.objects.all(),
            "timeline_steps": TimelineStep.objects.all(),
            "services_faqs": ServicesFaq.objects.all(),
        }
    )
    return render(request, "home/services.html", context)


def pricing(request):
    context = site_context(
        "Pricing | Bwire Global Tech",
        "Explore the web development packages, AI pricing, and add-on services.",
        "pricing",
    )
    context.update(
        {
            "pricing_hero": PricingHero.objects.first(),
            "pricing_packages": PricingPackage.objects.all(),
            "pricing_addons": PricingAddon.objects.all(),
            "pricing_terms": PricingTerms.objects.first(),
            "pricing_cta": PricingCta.objects.first(),
        }
    )
    return render(request, "home/pricing.html", context)


def portfolio(request):
    context = site_context(
        "Portfolio | Bwire Global Tech",
        "See sample case studies and project outcomes built for a modern digital brand.",
        "portfolio",
    )
    context.update(
        {
            "portfolio_hero": PortfolioHero.objects.first(),
            "portfolio_items": PortfolioItem.objects.all(),
            "portfolio_outcomes": PortfolioOutcome.objects.all(),
            "portfolio_deep_dive": PortfolioDeepDive.objects.first(),
            "portfolio_deep_dive_metrics": PortfolioDeepDiveMetric.objects.all(),
        }
    )
    return render(request, "home/portfolio.html", context)


def contact(request):
    form = ContactForm(request.POST or None, request.FILES or None)
    submitted = False
    contact_hero = ContactHero.objects.first()

    if request.method == "POST" and form.is_valid():
        cleaned = form.cleaned_data
        ProjectRequest.objects.create(
            full_name=cleaned["full_name"],
            email=cleaned["email"],
            phone=cleaned["phone"],
            project_type=cleaned["project_type"],
            message=cleaned["message"],
            budget_range=cleaned.get("budget_range", ""),
            timeline=cleaned.get("timeline", ""),
            referral_source=cleaned.get("referral_source", ""),
            reference_file=cleaned.get("reference_file"),
        )

        admin_subject = f"New project request: {cleaned['full_name']}"
        admin_message = (
            f"Full name: {cleaned['full_name']}\n"
            f"Email: {cleaned['email']}\n"
            f"Phone: {cleaned['phone']}\n"
            f"Project type: {cleaned['project_type']}\n"
            f"Budget range: {cleaned.get('budget_range') or 'Not provided'}\n"
            f"Timeline: {cleaned.get('timeline') or 'Not provided'}\n"
            f"Referral source: {cleaned.get('referral_source') or 'Not provided'}\n\n"
            "Project description:\n"
            f"{cleaned['message']}\n"
        )
        admin_email = EmailMessage(
            subject=admin_subject,
            body=admin_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_EMAIL],
            reply_to=[cleaned["email"]],
        )
        admin_email.send(fail_silently=not settings.DEBUG)

        visitor_subject = "We received your project request"
        visitor_message = (
            "Thanks for reaching out to Bwire Global Tech.\n\n"
            "We have received your project request and will get back to you within 24 hours.\n"
            "If you need to add more details, just reply to this email."
        )
        send_mail(
            visitor_subject,
            visitor_message,
            settings.DEFAULT_FROM_EMAIL,
            [cleaned["email"]],
            fail_silently=not settings.DEBUG,
        )
        submitted = True
        form = ContactForm()

    context = site_context(
        "Contact | Bwire Global Tech",
        "Start a project with Bwire Global Tech through a direct contact form and project brief.",
        "contact",
    )
    context.update(
        {
            "form": form,
            "submitted": submitted,
            "contact_hero": contact_hero,
            "contact_checklist": ContactChecklistItem.objects.all(),
            "contact_next_steps": ContactNextStep.objects.all(),
        }
    )
    return render(request, "home/contact.html", context)


def terms(request):
    context = site_context(
        "Terms of Use | Bwire Global Tech",
        "Review the Bwire Global Tech terms of use, service scope, and payment policies.",
        "terms",
    )
    context["terms_page"] = TermsPage.objects.first()
    return render(request, "home/terms.html", context)


def privacy(request):
    context = site_context(
        "Privacy Policy | Bwire Global Tech",
        "Read the Bwire Global Tech privacy policy and data handling practices.",
        "privacy",
    )
    context["privacy_page"] = PrivacyPage.objects.first()
    return render(request, "home/privacy.html", context)


@require_POST
@csrf_protect
def chat_ai(request):

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return JsonResponse({"error": "Missing OPENAI_API_KEY."}, status=500)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    user_message = (payload.get("message") or "").strip()
    history = payload.get("history") or []

    if not user_message:
        return JsonResponse({"error": "Message is required."}, status=400)

    client = OpenAI(api_key=api_key)
    system_prompt = (
        "You are Lee, the assistant for the Bwire Global Tech website. "
        "Use ONLY the site context provided. "
        "First, make sure you understand the visitor's request; if it is vague, ask a short clarifying question. "
        "Avoid generic filler and keep responses concise and specific to Bwire Global Tech. "
        "If the answer is not in the context, say you do not know and ask the visitor "
        "to contact the team via email or phone."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Site context:\n{SITE_CONTEXT}"},
    ]

    for item in history[-8:]:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
    )

    answer = response.choices[0].message.content.strip()
    return JsonResponse({"answer": answer})
