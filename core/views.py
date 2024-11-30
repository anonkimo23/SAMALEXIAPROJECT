from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import Observacion, ImagenDescripcion
from .forms import ImagenDescripcionForm
from .models import Grado, Estudiante
from django.shortcuts import get_object_or_404, redirect

def profesor_observador(request):
    cursos = Grado.objects.all()
    estudiantes = []
    observaciones = []

    # Obtener el curso seleccionado (si existe)
    curso_id = request.GET.get('curso')
    estudiante_id = request.GET.get('estudiante')

    if curso_id:
        estudiantes = Estudiante.objects.filter(grado_id=curso_id)

    if estudiante_id:
        observaciones = Observacion.objects.filter(estudiante_id=estudiante_id)

    return render(request, 'profesor_observador.html', {
        'cursos': cursos,
        'estudiantes': estudiantes,
        'observaciones': observaciones,
        'curso_seleccionado': curso_id,
        'estudiante_seleccionado': estudiante_id,
    })


# Vista para la página principal
def principal_home(request):
    return render(request, 'principal_home.html')


# Vista para el login
def login_app(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirige según el tipo de usuario
            if hasattr(user, 'estudiante'):
                return redirect('estudiantes_home')
            elif hasattr(user, 'profesor'):
                return redirect('profesores_home')
            else:
                return redirect('principal_home')  # Página predeterminada
        else:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'login_app.html')

    return render(request, 'login_app.html')


# Vista para estudiantes
def estudiantes_home(request):
    eventos = ImagenDescripcion.objects.all().order_by('-fecha_creacion')
    return render(request, 'estudiantes_home.html', {'eventos': eventos})


# Vista para profesores
def profesores_home(request):
    if request.method == 'POST':
        form = ImagenDescripcionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Contenido publicado con éxito!')
            return redirect('profesores_home')
        else:
            messages.error(request, 'Ocurrió un error. Verifica el formulario.')
    else:
        form = ImagenDescripcionForm()

    publicaciones = ImagenDescripcion.objects.all().order_by('-fecha_creacion')
    return render(request, 'profesores_home.html', {'form': form, 'publicaciones': publicaciones})


# Vista para eliminar publicaciones
def eliminar_publicaciones(request):
    if request.method == 'POST':
        ids_a_eliminar = request.POST.getlist('eliminar[]')
        if ids_a_eliminar:
            ImagenDescripcion.objects.filter(id__in=ids_a_eliminar).delete()
            messages.success(request, 'Publicaciones eliminadas con éxito.')
        else:
            messages.warning(request, 'No seleccionaste ninguna publicación.')
    return redirect('profesores_home')


# Vista para eventos de estudiantes
def eventos_estudiantes(request):
    eventos = ImagenDescripcion.objects.all().order_by('-fecha_creacion')
    return render(request, 'eventos_estudiantes.html', {'eventos': eventos})


# Vista para manual de convivencia
def manual_convivencia(request):
    return render(request, 'manual_convivencia.html')


# Vista para recuperación de contraseña
def olvido_contrasena(request):
    return render(request, 'olvido_contrasena.html')


# Vista para observador de estudiantes
def estudiantes_observador(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        descripcion = data.get('descripcion')
        estudiante_id = data.get('estudiante_id')

        if descripcion and estudiante_id:
            # Guardar la nueva observación en la base de datos
            nueva_observacion = Observacion.objects.create(
                descripcion=descripcion,
                fecha=datetime.now(),
                estudiante_id=estudiante_id
            )
            return JsonResponse({
                'success': True,
                'descripcion': nueva_observacion.descripcion,
                'fecha': nueva_observacion.fecha.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'success': False, 'error': 'Datos inválidos.'})

    # Obtener todas las observaciones relacionadas con un estudiante (filtrar por estudiante_id)
    estudiante_id = request.GET.get('estudiante_id')  # Filtrar por estudiante si corresponde
    observaciones = Observacion.objects.filter(estudiante_id=estudiante_id) if estudiante_id else Observacion.objects.all()
    return render(request, 'estudiantes_observador.html', {'observaciones': observaciones})


# Vista para observador de profesores
from django.shortcuts import render
from .models import Grado, Estudiante, Observacion

def profesor_observador(request):
    cursos = Grado.objects.all()  # Obtener todos los cursos
    curso_seleccionado = request.GET.get('curso', '')  # Obtener el curso seleccionado
    estudiante_seleccionado = request.GET.get('estudiante', '')  # Obtener el estudiante seleccionado
    
    estudiantes = []
    observaciones = []

    # Validar si el curso seleccionado es un número válido
    if curso_seleccionado.isdigit():
        estudiantes = Estudiante.objects.filter(grado_id=curso_seleccionado)  # Filtrar estudiantes por curso seleccionado

    # Validar si el estudiante seleccionado es un número válido
    if estudiante_seleccionado.isdigit():
        observaciones = Observacion.objects.filter(estudiante_id=estudiante_seleccionado)  # Filtrar observaciones por estudiante seleccionado

    # Manejar el formulario de envío de observaciones
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion', '').strip()
        estudiante_id = request.POST.get('estudiante_id', '')

        if descripcion and estudiante_id.isdigit():
            Observacion.objects.create(
                descripcion=descripcion,
                estudiante_id=estudiante_id
            )

    return render(request, 'profesor_observador.html', {
        'cursos': cursos,
        'curso_seleccionado': curso_seleccionado,
        'estudiantes': estudiantes,
        'estudiante_seleccionado': estudiante_seleccionado,
        'observaciones': observaciones,
    })




def cursos(request):
    return render(request, 'cursos.html')



# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('principal_home')

def borrar_observacion(request, observacion_id):
    if request.method == 'POST':
        observacion = get_object_or_404(Observacion, id=observacion_id)
        observacion.delete()
        messages.success(request, 'Observación eliminada con éxito.')
    return redirect('profesor_observador')






