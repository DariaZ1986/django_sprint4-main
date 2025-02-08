from django.urls import include, path

from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('', include('django.contrib.auth.urls')),
]
