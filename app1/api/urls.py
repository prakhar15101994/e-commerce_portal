from django.urls import path, include

from app1.api import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('curd', views.ProductViewSet, basename='Product')

urlpatterns=[
    path('', include(router.urls))
]