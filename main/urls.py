
from django.urls import path
from django.conf.urls import include
from main import views


urlpatterns = [
        path('', views.IndexView.as_view(), name='index'),
        path('query/<page_number>', views.QueryView.as_view(), name='query'),
        path('info', views.InfoView.as_view(), name='info')
]
