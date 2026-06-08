import json
import os
import logging

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

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
    GalleryMedia,
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
    ServiceItem,
    ServicesFaq,
    ServicesHero,
    SiteSettings,
    TermsPage,
    TimelineStep,
)
from .services import site_context, create_project_request, build_contact_emails, build_chat_messages
from .tasks import send_email_task, call_openai_chat
from .utils import rate_limit, get_client_ip
from openai import OpenAI

logger = logging.getLogger("home.views")


@cache_page(60)
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
            "home_case_studies": HomeCaseStudy.objects.prefetch_related("media_items"),
            "home_testimonials": HomeTestimonial.objects.all(),
            "home_faqs": HomeFaq.objects.all(),
            "home_cta": HomeCta.objects.first(),
        }
    )
    return render(request, "home/index.html", context)


@cache_page(60)
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


@cache_page(60)
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


@cache_page(60)
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


@cache_page(60)
def portfolio(request):
    context = site_context(
        "Portfolio | Bwire Global Tech",
        "See sample case studies and project outcomes built for a modern digital brand.",
        "portfolio",
    )
    category = request.GET.get("category")
    sort = request.GET.get("sort", "order")
    items = PortfolioItem.objects.prefetch_related("media_items")
    if category:
        items = items.filter(category=category)
    if sort == "title":
        items = items.order_by("title")
    else:
        items = items.order_by("order", "id")

    paginator = Paginator(items, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context.update(
        {
            "portfolio_hero": PortfolioHero.objects.first(),
            "portfolio_items": page_obj,
            "portfolio_outcomes": PortfolioOutcome.objects.all(),
            "portfolio_deep_dive": PortfolioDeepDive.objects.first(),
            "portfolio_deep_dive_metrics": PortfolioDeepDiveMetric.objects.all(),
            "portfolio_categories": PortfolioItem.CATEGORY_CHOICES,
            "active_category": category,
            "active_sort": sort,
        }
    )
    return render(request, "home/portfolio.html", context)


@cache_page(60)
def portfolio_detail(request, pk):
    item = get_object_or_404(PortfolioItem.objects.prefetch_related("media_items"), pk=pk)
    context = site_context(
        f"{item.title} | Portfolio | Bwire Global Tech",
        item.body,
        "portfolio",
    )
    context["item"] = item
    return render(request, "home/portfolio_detail.html", context)


@cache_page(60)
def gallery(request):
    context = site_context(
        "Gallery | Bwire Global Tech",
        "Explore images and videos from recent web and AI projects by Bwire Global Tech.",
        "gallery",
    )
    context["gallery_media"] = GalleryMedia.objects.all()
    return render(request, "home/gallery.html", context)


@rate_limit(limit=6, period=60)
def contact(request):
    form = ContactForm(request.POST or None, request.FILES or None)
    submitted = False
    contact_hero = ContactHero.objects.first()

    if request.method == "POST":
        if form.is_valid():
            try:
                with transaction.atomic():
                    create_project_request(form.cleaned_data)

                admin_email, visitor_email = build_contact_emails(
                    form.cleaned_data, form.cleaned_data["email"]
                )

                if hasattr(send_email_task, "apply_async"):
                    send_email_task.apply_async(
                        (
                            admin_email.subject,
                            admin_email.body,
                            admin_email.from_email,
                            admin_email.to,
                            admin_email.reply_to,
                        )
                    )
                    send_email_task.apply_async(
                        (
                            visitor_email.subject,
                            visitor_email.body,
                            visitor_email.from_email,
                            visitor_email.to,
                            visitor_email.reply_to,
                        )
                    )
                else:
                    send_email_task(
                        admin_email.subject,
                        admin_email.body,
                        admin_email.from_email,
                        admin_email.to,
                        admin_email.reply_to,
                    )
                    send_email_task(
                        visitor_email.subject,
                        visitor_email.body,
                        visitor_email.from_email,
                        visitor_email.to,
                        visitor_email.reply_to,
                    )
                submitted = True
            except Exception as exc:
                logger.exception("Failed to process contact request: %s", exc)
        else:
            logger.warning("Contact form validation failed: %s", form.errors.as_json())

    context = site_context(
        "Contact | Bwire Global Tech",
        "Share your project goals, timeline, and ideas with Bwire Global Tech.",
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


@cache_page(60)
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


@rate_limit(limit=12, period=60)
@require_POST
@csrf_protect
def chat_ai(request):
    api_key = settings.OPENAI_API_KEY
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

    messages = build_chat_messages(user_message, history)
    response = None

    if hasattr(call_openai_chat, "apply_async"):
        try:
            task = call_openai_chat.apply_async((messages,), {"model": "gpt-4o-mini", "temperature": 0.3})
            task_result = task.get(timeout=15)
            if not task_result.get("ok"):
                logger.error("call_openai_chat task failed: %s", task_result.get("error"))
                return JsonResponse({"error": "AI service unavailable"}, status=503)
            response = task_result["response"]
        except Exception as exc:
            logger.exception("OpenAI task error: %s", exc)
            return JsonResponse({"error": "AI service unavailable"}, status=503)
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
            )
        except Exception as exc:
            logger.exception("OpenAI API error: %s", exc)
            return JsonResponse({"error": "AI service unavailable"}, status=503)

    try:
        answer = response.choices[0].message.content.strip()
    except Exception:
        logger.exception("Unexpected OpenAI response structure: %s", getattr(response, "__dict__", response))
        return JsonResponse({"error": "AI response error"}, status=502)

    logger.info("chat_ai used ip=%s", get_client_ip(request))
    return JsonResponse({"answer": answer})
