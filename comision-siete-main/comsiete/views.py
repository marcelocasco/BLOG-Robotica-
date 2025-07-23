# Solicitud HTTP
# Solicitudes entrantes -> request
# Devolver respuestas -> response
from django.shortcuts import render

# Devolver la página principal de mi sitio.
def inicio(request):
    return render(request, 'index.html')
