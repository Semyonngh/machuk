from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('tickets/', views.tickets, name='tickets'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('buy-ticket/<int:concert_id>/', views.buy_ticket, name='buy_ticket'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

]