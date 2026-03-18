import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Obra, Compositor
from .forms import ObraForm, RegistroForm, CompositorForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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
            return redirect('detalle_obra', obra_id=obra.id)
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
            return redirect('catalogo/lista_compositores')
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