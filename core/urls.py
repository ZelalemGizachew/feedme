from django.urls import path
from django.urls.conf import include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('users', views.UserViewSet, basename='user')
router.register(r'business-closings', views.BusinessClosingViewSet, basename='businessclosing')

urlpatterns = [
    path("feedme/", include(router.urls))
]