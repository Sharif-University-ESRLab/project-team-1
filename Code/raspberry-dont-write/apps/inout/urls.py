from django.urls import path

from . import views

app_name = 'inout'
urlpatterns = [
    path('getspeed/', views.get_speed, name='get-speed'),
]