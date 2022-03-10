"""FSDUAsigmaproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from .views import home_view,auth_view,verify_view,LandingView,Evaluation,download
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('',LandingView.as_view(),name='landing'),
    path('evaluation/',Evaluation.as_view(),name='evaluation'),
    path('evaluation-platform-admin-89967q89rp', admin.site.urls, ),
    path('home/',home_view, name='home-view'),
    path('verify/', verify_view, name='verify-view'),
    path('login/', auth_view, name='login-view'),
    path('users/', include('django.contrib.auth.urls')), 
    path('download-template/',download, name='download-template')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

