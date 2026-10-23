from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StaffViewSet

router=DefaultRouter()
router.register('', StaffViewSet, basename='staff')

urls_patterns = [
    path('', include(router.urls)),
]