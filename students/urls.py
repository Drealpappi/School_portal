from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, EnrollmentViewSet

router = DefaultRouter()

router.register('enrollments', EnrollmentViewSet, basename='enrollments')
router.register('', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(router.urls)),
]