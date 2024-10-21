from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileViewSet
# Create a router and register the viewset
router = DefaultRouter()
router.register(r'', FileViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
