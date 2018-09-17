from django.forms import ModelForm
from .models import ImageUpload


class UploadForm(ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image', 'lang']
        labels = {
            'lang':'Язык',
            'image':''
        }
