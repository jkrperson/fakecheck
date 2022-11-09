import requests, pyrebase
from urllib.parse import urlparse

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views import View
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from fakecheck.models import ThreatDomain, NewsArticle, NewsURL
from fakecheck.serializer import ThreatDomainSerializer, NewsArticleSerializer, NewsUrlSerializer


# Create your views here.
class AdminURLAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):

        if request.query_params.get("pk"):

            url_pk = request.query_params["pk"]

            try:
                news_object = NewsURL.objects.get(pk=url_pk)
                news_url_serializer = NewsUrlSerializer(news_object)
                return Response(data=news_url_serializer.data, status=status.HTTP_200_OK)

            except NewsURL.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif request.query_params.get("pagination"):

            limit = 10

            if request.query_params.get("limit"):
                limit = int(request.query_params["limit"])

            page = 1

            if request.query_params.get("page"):
                page = int(request.query_params["page"])

            newsobject = NewsURL.objects.all().order_by('date_reported')
            paginator = Paginator(newsobject, limit)
            news = paginator.page(page)
            news_url_serializer = NewsUrlSerializer(data=news, many=True)
            news_url_serializer.is_valid()

            return Response(data=news_url_serializer.data, status=status.HTTP_200_OK)

        else:

            limit = 3

            if request.query_params.get("limit"):
                limit = int(request.query_params["limit"])

            news = NewsURL.objects.all().order_by('date_reported')[:limit]
            news_url_serializer = NewsUrlSerializer(data=news, many=True)
            news_url_serializer.is_valid()

            return Response(data=news_url_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        news_url = request.data["news_url"]
        domain = request.data["domain"]


class AdminArticleAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):

        if request.query_params.get("pk"):

            article_pk = request.query_params["pk"]

            try:
                news_article_object = NewsArticle.objects.get(pk=article_pk)
                news_article_serializer = NewsArticleSerializer(news_article_object)
                return Response(data=news_article_serializer.data, status=status.HTTP_200_OK)

            except NewsArticle.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        elif request.query_params.get("Pagination"):

            limit = 10

            if request.query_params.get("limit"):
                limit = int(request.query_params["limit"])

            page = 1

            if request.query_params.get("page"):
                page = int(request.query_params["page"])

            news_article_object = NewsArticle.objects.all()
            paginator = Paginator(news_article_object, limit)
            news = paginator.page(page)
            news_article_serializer = NewsArticleSerializer(data=news, many=True)
            news_article_serializer.is_valid()

            return Response(data=news_article_serializer.data, status=status.HTTP_200_OK)

        else:

            limit = 3

            if request.query_params.get("limit"):
                limit = int(request.query_params["limit"])

            news = NewsArticle.objects.all().order_by('date_reported')[:limit]
            news_article_serializer = NewsArticleSerializer(data=news, many=True)
            news_article_serializer.is_valid()

            return Response(data=news_article_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        pass
#       TODO


class AdminDomainAPI(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):

        if request.query_params.get("pk"):

            domain_pk = request.query_params["pk"]

            try:
                domain_object = ThreatDomain.objects.get(pk=domain_pk)
                threat_domain_serializer = ThreatDomainSerializer(domain_object)
                threat_domain_serializer.is_valid()
                return Response(data=threat_domain_serializer.data, status=status.HTTP_200_OK)

            except ThreatDomain.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:

            limit = 10

            if request.query_params.get("limit"):
                limit = int(request.query_params["limit"])

            page = 1

            if request.query_params.get("page"):
                page = int(request.query_params["page"])

            domain_object = ThreatDomain.objects.all()
            paginator = Paginator(domain_object, limit)
            news = paginator.page(page)
            thread_domain_serializer = ThreatDomainSerializer(data=news, many=True)
            thread_domain_serializer.is_valid()

            return Response(data=thread_domain_serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        pass
#         TODO


class AdminSignIn(View):

    @staticmethod
    def get(request):
        return render(request=request, template_name="admin_signin.html")

    @staticmethod
    def post(request):

        try:
            username = request.data["username"]
            password = request.data["password"]

            print(username, password)

        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


