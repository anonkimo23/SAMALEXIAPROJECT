from django.db import models
from django.contrib.auth.models import User
from django import forms


# Modelo de Grado
class Grado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name='estudiantes')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# Modelo de Profesor
class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profesor")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)  # Ej: "Matemáticas", "Ciencias Naturales"
    identificacion = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


# Modelo de Asignatura
class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="asignaturas")
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, blank=True, related_name="asignaturas")

    def __str__(self):
        return self.nombre


# Modelo de Nota
class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="notas")
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="notas")
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)  # Ej: 4.5, 3.0
    observacion = models.TextField(blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.estudiante} - {self.asignatura} - {self.calificacion}"


# Modelo de Observación
class Observacion(models.Model):
    descripcion = models.TextField(default="Sin descripción")
    fecha = models.DateTimeField(auto_now_add=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="observaciones")

    def __str__(self):
        return f"Observación de {self.estudiante} - {self.fecha}"




# Modelo de Imagen y Descripción
class ImagenDescripcion(models.Model):
    titulo = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    imagen1 = models.ImageField(upload_to='imagenes/')
    imagen2 = models.ImageField(upload_to='imagenes/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or "Sin título"


# Formulario relacionado con ImagenDescripcion
class ImagenDescripcionForm(forms.ModelForm):
    class Meta:
        model = ImagenDescripcion
        fields = ['titulo', 'descripcion', 'imagen1', 'imagen2']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la descripción del evento',
                'rows': 4
            }),
            'imagen1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class Observacion(models.Model):
    descripcion = models.TextField(default="Sin descripción")  # Predeterminado para descripciones vacías
    fecha = models.DateTimeField(auto_now_add=True)  # Predeterminado a la fecha y hora actual
    estudiante_id = models.IntegerField(default=0)  # Valor predeterminado para identificador del estudiante

    def __str__(self):
        return f"Observación del estudiante {self.estudiante_id} - {self.fecha}"
    
