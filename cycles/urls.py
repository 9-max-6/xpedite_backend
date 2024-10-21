from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CycleViewSet, SuperCycleViewSet

router = DefaultRouter()
router.register(r'cycles', CycleViewSet, basename='cycles')
router.register(r'super-cycles', SuperCycleViewSet, basename='supercycle')

urlpatterns = [
    path('', include(router.urls)),
]
