"""REST_IA_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from server import views
from django.conf import settings, urls


router = routers.DefaultRouter()
router.register(r'typeelements', views.TypeElementViewSet, basename='typeelement')
router.register(r'elements', views.ElementViewSet, basename='element')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'owners', views.OwnerViewSet, basename='owner')
router.register(r'applications', views.ApplicationViewSet, basename='application')
router.register(r'visites', views.VisiteViewSet, basename='visite')
router.register(r'typepages', views.TypePageViewSet, basename='typepage')
router.register(r'pages', views.PageViewSet, basename='page')
router.register(r'actions', views.ActionViewSet, basename='action')
router.register(r'typeactions', views.TypeActionViewSet, basename='typeaction')
router.register(r'pertinences', views.PertinenceViewSet, basename='pertinence')


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls)
    # urls.url('^pertinent/(?P<application_id>.+)$', views.RefuseDemandeAPIView.as_view()),
]
