import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Obra, Compositor, Reporte
from .forms import ObraForm, RegistroForm, CompositorForm, ReporteForm, UsuarioAdminForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages

def lista_obras(request):
    query = request.GET.get('q')
    compositor_id = request.GET.get('compositor')
    tipo = request.GET.get('tipo')
    orden = request.GET.get('orden')
    
    obras = Obra.objects.all()
    compositores = Compositor.objects.all()

    if query:
        obras = obras.filter(titulo__icontains=query)
    if compositor_id:
        obras = obras.filter(compositor_id=compositor_id)
    if tipo:
        obras = obras.filter(tipo=tipo)

    if orden == 'duracion':
        obras = obras.order_by('-duracion_minutos')
    elif orden == 'antiguedad':
        obras = obras.order_by('ano_composicion')
    else:
        obras = obras.order_by('-popularidad')

    contexto = {
        'obras': obras,
        'compositores': compositores,
        'tipos_obra': Obra.TIPOS_DE_OBRA,
        'query': query,
        'compositor_seleccionado': compositor_id,
        'tipo_seleccionado': tipo,
        'orden_seleccionado': orden,
    }
    
    return render(request, 'catalogo/lista_obras.html', contexto)

def detalle_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    obra.popularidad += 1
    obra.save()
    return render(request, 'catalogo/detalle_obra.html', {'obra': obra})

@login_required 
def nueva_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES)
        if form.is_valid():
            obra = form.save(commit=False)
            obra.creador = request.user
            obra.save()
            return redirect('lista_obras')
    else:
        form = ObraForm()
    
    return render(request, 'catalogo/obra_form.html', {'form': form})

@login_required
def editar_obra(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    
    if request.user != obra.creador and not request.user.is_superuser:
        raise PermissionDenied("No tienes permiso para editar esta obra.")
        
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES, instance=obra)
        if form.is_valid():
            form.save()
            reporte_id = request.GET.get('reporte')
            if reporte_id:
                try:
                    reporte_obj = Reporte.objects.get(id=reporte_id)
                    reporte_obj.resuelto = True
                    reporte_obj.save()
                except Reporte.DoesNotExist:
                    pass
            
            return redirect('lista_obras') 
    else:
        form = ObraForm(instance=obra)
        
    return render(request, 'catalogo/obra_form.html', {'form': form, 'obra': obra})

def lista_compositores(request):
    compositores = Compositor.objects.all().order_by('nombre')
    return render(request, 'catalogo/lista_compositores.html', {'compositores': compositores})

def detalle_compositor(request, compositor_id):
    compositor = get_object_or_404(Compositor, id=compositor_id)
    return render(request, 'catalogo/detalle_compositor.html', {'compositor': compositor})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('lista_obras')
    else:
        form = RegistroForm()
    return render(request, 'catalogo/registro.html', {'form': form})

@login_required
def nuevo_compositor(request):
    if request.method == 'POST':
        form = CompositorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_compositores')
    else:
        form = CompositorForm()
    return render(request, 'catalogo/nuevo_compositor.html', {'form': form})

@login_required
def eliminar_compositor(request, compositor_id):
    if not request.user.is_superuser:
        return redirect('lista_compositores')

    compositor = get_object_or_404(Compositor, id=compositor_id)

    if request.method == 'POST':
        compositor.delete()
        return redirect('lista_compositores')

    return render(request, 'catalogo/eliminar_compositor.html', {'compositor': compositor})


def vista_rocola(request):
    obras = Obra.objects.all()
    
    lista_canciones = []
    for obra in obras:
        # Usamos getattr para evitar errores si los campos no existen en tu models.py
        duracion_texto = getattr(obra, 'duracion', "—")
        compositor_obj = getattr(obra, 'compositor', None)
        audio_obj = getattr(obra, 'audio', None)
        
        lista_canciones.append({
            "id": obra.id,
            "title": obra.titulo,
            "artist": compositor_obj.nombre if compositor_obj else "Desconocido",
            "duration": duracion_texto,
            "audio_url": audio_obj.url if audio_obj else None,
        })
    
    canciones_json = json.dumps(lista_canciones)
    return render(request, 'catalogo/rocola.html', {'songs_json': canciones_json})

@login_required
def crear_reporte(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.obra = obra
            reporte.usuario = request.user
            reporte.save()
            return redirect('lista_obras') 
    else:
        form = ReporteForm()
        
    return render(request, 'catalogo/reporte_form.html', {'form': form, 'obra': obra})

# Función auxiliar de seguridad
def es_admin(user):
    return user.is_staff or user.is_superuser

# Vista para el inicio del CU-15 (Solo Administradores)
@user_passes_test(es_admin)
def bandeja_reportes(request):
    reportes = Reporte.objects.all().order_by('-fecha_creacion')
    return render(request, 'catalogo/bandeja_reportes.html', {'reportes': reportes})


@user_passes_test(es_admin)
def lista_usuarios(request):
    from django.contrib.auth.models import User
    usuarios = User.objects.all().order_by('username')
    return render(request, 'catalogo/lista_usuarios.html', {'usuarios': usuarios})

@user_passes_test(es_admin)
def editar_usuario(request, usuario_id):
    from django.contrib.auth.models import User
    from .forms import EditarUsuarioForm
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'catalogo/editar_usuario.html', {'form': form, 'usuario': usuario})

@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    from django.contrib.auth.models import User
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'catalogo/eliminar_usuario.html', {'usuario': usuario})


class CustomLoginView(LoginView):
    template_name = 'catalogo/login.html'

    def form_invalid(self, form):
        username = form.data.get('username')
        if username:
            from django.contrib.auth.models import User
            try:
                usuario = User.objects.get(username=username)
                if not usuario.is_active:
                    messages.error(self.request, 'Tu cuenta está desactivada. Contacta con el administrador.')
            except User.DoesNotExist:
                pass
        return super().form_invalid(form)