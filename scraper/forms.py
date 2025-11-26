from django import forms

class ScraperForm(forms.Form):
    palabra = forms.CharField(label="Palabra clave", max_length=50)
