from django import forms
from .models import Prestamo
from lectores.models import Lector
from libros.models import Libro
from datetime import date

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['lector', 'libro', 'fecha_limite', 'observaciones']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'lector': forms.Select(attrs={'class': 'form-select'}),
            'libro': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo lectores activos
        self.fields['lector'].queryset = Lector.objects.filter(activo=True)
        # Filtrar solo libros disponibles
        self.fields['libro'].queryset = Libro.objects.filter(estado='disponible')
    
    def clean(self):
        cleaned_data = super().clean()
        lector = cleaned_data.get('lector')
        libro = cleaned_data.get('libro')
        
        # Verificar que el lector no tenga préstamos vencidos
        if lector:
            prestamos_vencidos = Prestamo.objects.filter(
                lector=lector, 
                estado='activo',
                fecha_limite__lt=date.today()
            ).exists()
            if prestamos_vencidos:
                raise forms.ValidationError("El lector tiene préstamos vencidos")
        
        return cleaned_data

class DevolucionForm(forms.Form):
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=False,
        label='Observaciones de la devolución'
    )