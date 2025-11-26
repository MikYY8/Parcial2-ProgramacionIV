import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.http import HttpResponse
from .forms import ScraperForm
from django.core.mail import send_mail

def buscar(request):
    form = ScraperForm()
    return render(request, "scraper/buscar.html", {"form": form})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import requests

def resultado(request):
    # DEBUG: imprimimos en consola para verificar si llega el POST
    print(">>> resultado view - método:", request.method)

    if request.method != "POST":
        return HttpResponse(
            "DEBUG: Esta vista espera POST. Si ves esto, el formulario no está enviando correctamente.",
            status=200,
        )

    # Llegó POST: verificamos el campo
    palabra = request.POST.get("palabra")
    print(">>> palabra recibida:", repr(palabra))

    if not palabra:
        messages.error(request, "No enviaste ninguna palabra.")
        return redirect("scraper:buscar")

    # --- Scraping REAL usando la API de Wikipedia ---
    url = "https://es.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "exintro": True,
        "explaintext": True,
        "titles": palabra,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(">>> status code:", response.status_code)
        response.raise_for_status()  # lanza error si status != 200
    except requests.RequestException as e:
        print(">>> ERROR en request:", e)
        messages.error(request, "Error al conectarse a Wikipedia.")
        return redirect("scraper:buscar")

    try:
        data = response.json()
    except ValueError as e:
        print(">>> ERROR parseando JSON:", e)
        messages.error(request, "No se pudo procesar la respuesta de Wikipedia.")
        return redirect("scraper:buscar")

    page = next(iter(data["query"]["pages"].values()))
    if "extract" not in page or not page["extract"].strip():
        messages.error(request, "No se encontraron resultados.")
        return redirect("scraper:buscar")

    contenido = page["extract"].split(".")[:5]  # primeras 5 frases
    contenido = [c.strip() for c in contenido if c.strip()]

    if not contenido:
        messages.error(request, "No se encontraron resultados útiles.")
        return redirect("scraper:buscar")

    # Guardamos en sesión para enviar por mail
    request.session["scraper_palabra"] = palabra
    request.session["scraper_resultados"] = contenido

    return render(request, "scraper/resultado.html", {"palabra": palabra, "resultados": contenido})


def enviar_mail(request):
    return render(request, "enviar_mail.html")
