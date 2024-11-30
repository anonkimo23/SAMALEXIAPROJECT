from django.contrib import admin
from .models import Estudiante, Profesor, Grado

# Registro de modelos en el admin
admin.site.register(Grado)

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('user', 'grado')
    search_fields = ('user__username', 'grado__nombre')

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad')
    search_fields = ('user__username', 'especialidad')


# Register your models here.
