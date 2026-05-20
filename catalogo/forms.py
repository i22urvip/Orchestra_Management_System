from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Obra, Compositor, Reporte


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['titulo', 'compositor', 'tipo', 'ano_composicion', 'duracion_minutos', 'num_instrumentos', 'partitura']

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

class CompositorForm(forms.ModelForm):
    class Meta:
        model = Compositor
        fields = ['nombre', 'epoca', 'biografia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['epoca'].required = True
        self.fields['biografia'].required = True

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = '__all__'

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ['motivo']

class UsuarioAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'is_active': 'Usuario activo',
            'is_staff': 'Administrador',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name in ['is_active', 'is_staff']:
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']