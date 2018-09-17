from django.db import models
from django.contrib.sessions.models import Session
from PIL import Image
import pytesseract
import os


LANG_CHOICES = (
    ('rus', 'русский'),
    ('eng', 'english')
)


class ImageUpload(models.Model):
    image = models.ImageField(upload_to="images")
    lang = models.CharField(default="", max_length=15 , choices=LANG_CHOICES)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super(ImageUpload, self).delete(*args,**kwargs)

    def image_to_text(self):
        text = pytesseract.image_to_string(Image.open(self.image), lang=self.lang)
        return text


class UserQuery(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
