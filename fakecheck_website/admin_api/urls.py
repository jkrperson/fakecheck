from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from . import views

urlpatterns = [

    path('api/url/', views.AdminURLAPI.as_view(), name="Fakescore Page URL"),
    path('api/article/', views.AdminArticleAPI.as_view(), name="Fakescore Page Article"),
    path('signup', views.AdminSignIn.as_view(), name="Fake Check Signup")
]
