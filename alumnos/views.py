from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno
from django.core.mail import EmailMessage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
from io import BytesIO


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



def enviar_pdf(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)

    # --- Generar PDF en memoria ---
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 800, "Ficha del Alumno")

    p.setFont("Helvetica", 12)
    p.drawString(100, 760, f"Nombre: {alumno.nombre}")
    p.drawString(100, 740, f"Apellido: {alumno.apellido}")
    p.drawString(100, 720, f"DNI: {alumno.dni}")
    p.drawString(100, 700, f"Correo: {alumno.email}")

    p.showPage()
    p.save()

    pdf_value = buffer.getvalue()
    buffer.close()

    # --- Configurar email ---
    asunto = f"PDF del alumno {alumno.nombre}"
    cuerpo = "Adjunto se envía el PDF solicitado."
    destinatario = "docente@ejemplo.com"  # o alumno.email si querés

    email = EmailMessage(
        asunto,
        cuerpo,
        "noreply@tuapp.com",
        [destinatario],
    )

    email.attach(f"Alumno_{alumno.pk}.pdf", pdf_value, "application/pdf")
    email.send()

    messages.success(request, "PDF enviado correctamente.")
    return redirect("alumnos:lista")
