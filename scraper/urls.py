from django.urls import path
from . import views

app_name = "scraper"

urlpatterns = [
    path("", views.buscar, name="buscar"),
    path("resultado/", views.resultado, name="resultado"),
    path("enviar-email/", views.enviar_email, name="enviar_email"),
    path("test-email/", views.test_email, name="test_email"),
]
