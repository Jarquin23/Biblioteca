from django import forms
from .models import Lector

class LectorForm(forms.ModelForm):
    class Meta:
        model = Lector
        fields = ['nombre', 'apellidos', 'tipo_documento', 'numero_documento',
                 'email', 'telefono', 'direccion', 'fecha_nacimiento', 'observaciones']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_numero_documento(self):
        nro_doc = self.cleaned_data.get('numero_documento')
        if Lector.objects.filter(numero_documento=nro_doc).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este número de documento ya está registrado")
        return nro_doc