from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, instructors_list_create

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),                
    path('instructors/', instructors_list_create) 
]