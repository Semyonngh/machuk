from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'concerts', views.ConcertViewSet, basename='concert')
router.register(r'artists', views.ArtistViewSet, basename='artist')
router.register(r'venues', views.VenueViewSet, basename='venue')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/concerts/<int:concert_id>/buy/', views.buy_ticket, name='buy_ticket'),
    path('api/orders/<int:order_id>/', views.order_detail, name='order_detail'),
]