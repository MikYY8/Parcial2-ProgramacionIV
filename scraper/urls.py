from django.urls import path
from . import views

app_name = "scraper"

urlpatterns = [
    path("", views.buscar, name="buscar"),
    path("resultado/", views.resultado, name="resultado"),
    path("enviar-mail/", views.enviar_mail, name="enviar_mail"),
]
