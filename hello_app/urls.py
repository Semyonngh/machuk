from hello_app import views
from django.urls import path

urlpatterns = [
    path('', views.online, name='home'),
    path('tickets/', views.tickets, name='tickets'),  # ДОБАВЬТЕ ЭТУ СТРОКУ
]