from django import forms
from .models import ImagenDescripcion

class ImagenDescripcionForm(forms.ModelForm):
    class Meta:
        model = ImagenDescripcion
        fields = ['titulo', 'descripcion', 'imagen1', 'imagen2']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la descripción del evento',
                'rows': 4
            }),
            'imagen1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        # Llama a la limpieza estándar
        cleaned_data = super().clean()

        # Valida que ambas imágenes estén presentes
        if not cleaned_data.get('imagen1'):
            raise forms.ValidationError("Debes subir la primera imagen.")
        if not cleaned_data.get('imagen2'):
            raise forms.ValidationError("Debes subir la segunda imagen.")

        return cleaned_data
    
from .models import Observacion

class ObservacionForm(forms.ModelForm):
    class Meta:
        model = Observacion
        fields = ['descripcion', 'estudiante_id']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'placeholder': 'Escribe tu observación aquí...',
                'class': 'form-control',
                'rows': 3,
            }),
            'estudiante_id': forms.HiddenInput(),
        }
