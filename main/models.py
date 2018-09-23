from django.db import models
from django.contrib.sessions.models import Session
from ocr_site.settings import MEDIA_ROOT
from PIL import Image
import pytesseract
import cv2
import numpy as np
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
        self.img = MEDIA_ROOT + '/' + str(self.image)
        self.img = cv2.imread(self.img)
        self.img = cv2.resize(self.img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        self.kernel = np.ones((1, 1), np.uint8)
        self.img = cv2.dilate(self.img, self.kernel, iterations=1)
        self.img = cv2.erode(self.img, self.kernel, iterations=1)
        self.img = cv2.threshold(cv2.GaussianBlur(self.img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        self.text = pytesseract.image_to_string(self.img, lang=self.lang)
        return self.text


class UserQuery(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
