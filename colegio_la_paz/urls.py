from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.principal_home, name='principal_home'),  # Página principal
    path('login/', views.login_app, name='login_app'),  # Login
    path('estudiantes/', views.estudiantes_home, name='estudiantes_home'),  # Página de estudiantes
    path('profesores/', views.profesores_home, name='profesores_home'),  # Página de directivos
    path('manual-convivencia/', views.manual_convivencia, name='manual_convivencia'),  # Manual de convivencia
    path('olvido-contrasena/', views.olvido_contrasena, name='olvido_contrasena'),
    path('Observador/', views.estudiantes_observador, name='estudiantes_observador'),  # Observador estudiantes
    path('profesor-observador/', views.profesor_observador, name='profesor_observador'),  # Observador docente
    path('logout/', views.logout_view, name='logout'),
    path('eliminar/', views.eliminar_publicaciones, name='eliminar_publicaciones'),
    path('cursos/', views.cursos, name='cursos'),
    path('borrar-observacion/<int:observacion_id>/', views.borrar_observacion, name='borrar_observacion'),

]

# Configuración para servir archivos estáticos y de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
