from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('me/', views.me, name='me'),
    path('tech/', views.tech, name='tech'),
]