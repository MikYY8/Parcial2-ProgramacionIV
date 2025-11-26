from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from rest_framework import viewsets
from .forms import RegisterForm, LoginForm
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def home_view(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # email de bienvenida
            send_mail(
                subject="¡Bienvenido!",
                message=f"Hola {user.username}, gracias por registrarte.",
                from_email=None,
                recipient_list=[user.email],
            )

            messages.success(request, "Te registraste correctamente. Ya podés iniciar sesión.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def signout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")
