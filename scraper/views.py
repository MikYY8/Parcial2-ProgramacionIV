import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import ScraperForm


def buscar(request):
    form = ScraperForm()
    return render(request, "scraper/buscar.html", {"form": form})


def resultado(request):
    if request.method == "POST":
        palabra = request.POST.get("palabra")

        # --- Scraping básico a Wikipedia ---
        url = f"https://es.wikipedia.org/wiki/{palabra}"
        response = requests.get(url)

        if response.status_code != 200:
            messages.error(request, "No se encontraron resultados.")
            return redirect("scraper:buscar")

        soup = BeautifulSoup(response.text, "html.parser")

        # Tomamos los primeros párrafos del artículo
        contenido = []
        for p in soup.select("p")[:3]:
            contenido.append(p.get_text())

        # Guardamos en sesión para enviar por mail
        request.session["scraper_palabra"] = palabra
        request.session["scraper_resultados"] = contenido

        return render(
            request,
            "scraper/resultado.html",
            {"palabra": palabra, "resultados": contenido},
        )

    return redirect("scraper:buscar")


def enviar_email(request):
    palabra = request.session.get("scraper_palabra")
    resultados = request.session.get("scraper_resultados")

    if not palabra or not resultados:
        messages.error(request, "No hay resultados para enviar.")
        return redirect("scraper:buscar")

    cuerpo = f"Resultados del scraping para '{palabra}':\n\n"
    for r in resultados:
        cuerpo += "- " + r + "\n\n"

    email = EmailMessage(
        subject=f"Scraping: {palabra}",
        body=cuerpo,
        from_email="noreply@tuapp.com",
        to=["docente@ejemplo.com"],
    )

    email.send()

    messages.success(request, "Resultados enviados por correo.")
    return redirect("scraper:buscar")
