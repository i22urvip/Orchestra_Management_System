from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Obra, Compositor

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