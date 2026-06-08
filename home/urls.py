from django.urls import path

from .views import (
    about,
    chat_ai,
    contact,
    gallery,
    home,
    portfolio,
    portfolio_detail,
    pricing,
    privacy,
    services,
    terms,
)
from .api_docs import api_docs

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
    path("pricing/", pricing, name="pricing"),
    path("portfolio/", portfolio, name="portfolio"),
    path("portfolio/<int:pk>/", portfolio_detail, name="portfolio_detail"),
    path("gallery/", gallery, name="gallery"),
    path("contact/", contact, name="contact"),
    path("terms/", terms, name="terms"),
    path("privacy/", privacy, name="privacy"),
    path("api/", api_docs, name="api_docs"),
    path("api/chat/", chat_ai, name="chat_ai"),
]
