from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AcademicSessionViewSet, TermViewSet, ClassLevelViewSet, ClassRoomViewSet, SubjectViewSet, SubjectAllocationViewSet

router = DefaultRouter()
router.register('sessions', AcademicSessionViewSet, basename='sessions')
router.register('terms', TermViewSet, basename='terms')
router.register('class-levels', ClassLevelViewSet, basename='class-levels')
router.register('classrooms', ClassRoomViewSet, basename='classrooms')
router.register('subjects', SubjectViewSet, basename='subjects')
router.register('allocations', SubjectAllocationViewSet, basename='allocations')

urlpatterns = [
    path('', include(router.urls)),
]