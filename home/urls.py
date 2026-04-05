from django.urls import path

from .views import about, chat_ai, contact, home, portfolio, pricing, services


urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("services/", services, name="services"),
    path("pricing/", pricing, name="pricing"),
    path("portfolio/", portfolio, name="portfolio"),
    path("contact/", contact, name="contact"),
    path("api/chat/", chat_ai, name="chat_ai"),
]
