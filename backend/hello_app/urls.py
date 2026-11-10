from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'concerts', views.ConcertViewSet, basename='concert')
router.register(r'artists', views.ArtistViewSet, basename='artist')
router.register(r'venues', views.VenueViewSet, basename='venue')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/filters/', views.filter_options, name='filters'),
    path('api/concerts/<int:concert_id>/buy/', views.buy_ticket, name='buy_ticket'),
    path('api/orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('api/register/', views.register, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/', views.get_profile, name='get_profile'),
    path('api/profile/update/', views.update_profile, name='update_profile'),
    path('api/my-orders/', views.my_orders, name='my_orders'),
    path('api/my-tickets/', views.my_tickets, name='my_tickets'),
    path('api/my-favorites/', views.my_favorites, name='my_favorites'),

]