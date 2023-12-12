from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api.views import CustomerViewSet,ProductViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'products', ProductViewSet, basename='product')
urlpatterns = [
    path('', include(router.urls)),
]