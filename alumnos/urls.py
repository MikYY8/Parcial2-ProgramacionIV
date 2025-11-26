from django.urls import path
from . import views

app_name = "alumnos"

urlpatterns = [
    path("", views.alumno_list, name="list"),
    path("crear/", views.alumno_create, name="create"),
    path("<int:pk>/editar/", views.alumno_edit, name="edit"),
    path("<int:pk>/eliminar/", views.alumno_delete, name="delete"),
    path("<int:pk>/enviar-pdf/", views.enviar_pdf, name="enviar_pdf"),
]
