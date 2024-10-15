from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet

# Create a router and register the viewset
router = DefaultRouter()
router.register(r'', RequestViewSet, basename='requests')

urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
