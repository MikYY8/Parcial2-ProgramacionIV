from . import models
from .models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina los textos de ayuda automáticos
        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(
            username=cleaned_data.get("username"),
            password=cleaned_data.get("password")
        )

        if not user:
            raise forms.ValidationError("Usuario o contraseña incorrectos")

        cleaned_data["user"] = user
        return cleaned_data