from django import forms
from .models import ImageUpload


class UploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image', 'lang']
        labels = {
            'lang':'Язык',
            'image':''
        }
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'style': 'display: none',
                    'class': 'file-input'
                }
            ),
            'lang': forms.Select(
                attrs={
                    'class': 'custom-select col-sm-4'
                }
            )
        }
