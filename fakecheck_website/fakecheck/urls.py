from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from .views import *

urlpatterns = [
    path('urls/check/', URLCheckAPI.as_view(), name="URLCheckAPI"),
    path('urls/report/', URLReportAPI.as_view(), name="URLReportAPI"),
    path('articles/check/', ArticleCheckAPI.as_view(), name="ArticleCheckAPI"),
    path('articles/report/', ArticleReportAPI.as_view(), name="ArticleReportAPI"),
]
