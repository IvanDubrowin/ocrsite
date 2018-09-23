from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import UserQuery, ImageUpload


class MyAdminSite(AdminSite):
    site_header = 'OCR Admin'

admin_site = MyAdminSite(name='admin')
admin_site.register([UserQuery, ImageUpload, Session, User])
