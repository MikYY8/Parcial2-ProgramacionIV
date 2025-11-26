from django.urls import path
from . import views

app_name = "alumnos"

urlpatterns = [
    path("", views.alumno_list, name="list"),
    path("crear/", views.alumno_create, name="create"),
    path("<int:pk>/editar/", views.alumno_edit, name="edit"),
    path("<int:pk>/eliminar/", views.alumno_delete, name="delete"),
    path('<int:id>/pdf/', views.reporte_pdf, name='enviar_pdf'),
    path("test-email/", views.test_email, name="test_email"),
]
