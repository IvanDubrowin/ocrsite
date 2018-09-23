from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ocr_site import settings
from main.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include(('main.urls', 'main'), namespace='main')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
