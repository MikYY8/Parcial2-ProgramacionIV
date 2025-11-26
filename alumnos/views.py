from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.http import FileResponse, Http404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from .models import Reporte
from django.core.mail import send_mail


@login_required
def alumno_list(request):
    alumnos = Alumno.objects.filter(user=request.user)
    return render(request, "alumnos/list.html", {"alumnos": alumnos})


@login_required
def alumno_create(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        dni = request.POST.get("dni")

        Alumno.objects.create(
            user=request.user,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
        )
        return redirect("alumnos:list")

    return render(request, "alumnos/create.html")


@login_required
def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, user=request.user)

    if request.method == "POST":
        alumno.nombre = request.POST.get("nombre")
        alumno.apellido = request.POST.get("apellido")
        alumno.dni = request.POST.get("dni")
        alumno.save()
        return redirect("alumnos:list")

    return render(request, "alumnos/edit.html", {"alumno": alumno})


@login_required
def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, user=request.user)
    alumno.delete()
    return redirect("alumnos:list")

def reporte_pdf(request, id): 
    try:
        reporte = Reporte.objects.get(pk=id)
    except Reporte.DoesNotExist:
        raise Http404("Reporte no encontrado")

    # Creamos un buffer temporal
    buffer = BytesIO()

    # Crear PDF con ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 750, f"Reporte: {reporte.nombre}")

    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Fecha: {reporte.fecha}")

    # Texto del contenido (línea por línea)
    y = 680
    for linea in reporte.contenido.split("\n"):
        p.drawString(100, y, linea)
        y -= 20  # bajar línea

        # si se acaba la página
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 750

    # cerrar página
    p.showPage()
    p.save()

    # Volver a inicio del buffer
    buffer.seek(0)

    # Devolver el PDF como descarga
    return FileResponse(buffer, as_attachment=True,
                        filename=f"reporte_{reporte.id}.pdf")


def test_email(request):
    try:
        send_mail(
            subject="PRUEBA SENDGRID",
            message="Este correo fue enviado desde Django usando SendGrid.",
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            recipient_list=["mica.yaz03@gmail.com"],
        )
        return HttpResponse("Email enviado correctamente.")
    except Exception as e:
        return HttpResponse(f"ERROR ENVIANDO EMAIL: {e}")


# def enviar_pdf(request, pk):
#     alumno = get_object_or_404(Alumno, pk=pk)

#     # --- Generar PDF en memoria ---
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)

#     p.setFont("Helvetica-Bold", 20)
#     p.drawString(100, 800, "Ficha del Alumno")

#     p.setFont("Helvetica", 12)
#     p.drawString(100, 760, f"Nombre: {alumno.nombre}")
#     p.drawString(100, 740, f"Apellido: {alumno.apellido}")
#     p.drawString(100, 720, f"DNI: {alumno.dni}")


#     p.showPage()
#     p.save()

#     pdf_value = buffer.getvalue()
#     buffer.close()

#     # --- Enviar email al usuario logueado ---
#     destinatario = request.user.email  # 👈 Opción B (funciona SIEMPRE)

#     email = EmailMessage(
#         subject=f"PDF del alumno {alumno.nombre}",
#         body="Adjunto se envía el PDF solicitado.",
#         from_email="noreply@tuapp.com",
#         to=[destinatario],
#     )

#     email.attach(f"Alumno_{alumno.pk}.pdf", pdf_value, "application/pdf")
#     email.send()

#     messages.success(request, "PDF enviado correctamente.")
#     return redirect("alumnos:lista")
