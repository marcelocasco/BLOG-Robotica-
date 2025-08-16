
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('apps.noticias.urls')), # Noticias
	path('login/', auth_views.LoginView.as_view(template_name='noticias/login.html'), name='login'),
]

	# Esta configuración permite servir archivos de medios (imágenes, etc.) durante el desarrollo.
	# Cuando DEBUG está activado, Django va a usar esta ruta para mostrar los archivos subidos en MEDIA_ROOT.
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)