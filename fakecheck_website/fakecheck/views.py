from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views import View
from django.core.exceptions import EmptyResultSet

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from fakecheck.errors import SiteNotFound, ServiceTemporaryUnavailable
from fakecheck.models import ThreatDomain, NewsArticle, NewsURL, NewsURLContent
from fakecheck.serializer import ThreatDomainSerializer, NewsArticleSerializer, \
    NewsUrlSerializer, NewsUrlContentSerializer, NewsArticleContentSerializer
from fakecheck.data_fetching import fetch_fakescore, convert_fakescore, retrieve_article_content, get_domain
from fakecheck.queries import *


# Create your views here.
class URLCheckAPI(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def post(request):
        try:
            # TODO: create more intuitive checking for backend
            news_url = request.data["news_url"]
        except KeyError as e:
            return Response(data={"error": "incomplete keys: {0}".format(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            news_object = NewsURL.objects.get(news_url=news_url)
            news_content_object = NewsURLContent.objects.get(url=news_object)
            news_content_data = NewsUrlContentSerializer(news_content_object).data

            request_status = status.HTTP_206_PARTIAL_CONTENT if news_content_data["url"].get("url_valid") is None else status.HTTP_200_OK

            return Response(data=news_content_data, status=request_status)

        except NewsURL.DoesNotExist:
            # TODO: Create a flowchart to explain the flow.
            try:
                content = retrieve_article_content(news_url)
            except SiteNotFound:
                return Response(status=status.HTTP_404_NOT_FOUND)

            news_object = NewsURL(news_url=news_url)

            try:
                pred, prob = fetch_fakescore(content)
                prob = convert_fakescore(pred, prob)

                data = {
                    "url": news_object,
                    "article_content": content,
                    "model_prediction": pred,
                    "model_probability": prob
                }

                news_content_serializer = NewsUrlContentSerializer(NewsURLContent(**data))
                return Response(data=news_content_serializer.data, status=status.HTTP_202_ACCEPTED)

            except ServiceTemporaryUnavailable:
                return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)


class URLReportAPI(APIView):

    @staticmethod
    def get(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            # TODO: create more intuitive checking for backend
            article_content = request.data["article_content"]
            news_url = request.data["news_url"]
            pred = request.data["model_prediction"]
            prob = request.data["model_probability"]
        except KeyError as e:
            return Response(data={"error": "incomplete keys: {0}".format(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

        domain, created = ThreatDomain.objects.get_or_create(domain=get_domain(news_url))

        news_url_data = {
            "news_url": news_url,
            "domain": domain
        }

        news_urls_object = NewsURL(**news_url_data)
        news_urls_object.save()

        news_article_content_data = {
            "url": news_urls_object,
            "article_content": article_content,
            "model_prediction": pred,
            "model_probability": prob
        }

        news_article_content_object = NewsURLContent(**news_article_content_data)
        news_article_content_object.save()
        return Response(status=status.HTTP_201_CREATED)


class ArticleCheckAPI(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def post(request):
        try:
            # TODO: create more intuitive checking for backend
            news = request.data["news_article"]

        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        try:        
            news_article_query = NewsArticle.objects.get(create_query_article(news))
            news_article_serializer = NewsArticleSerializer(news_article_query)
            request_status = status.HTTP_206_PARTIAL_CONTENT if news_article_query.article_valid is None else status.HTTP_200_OK
            return Response(data=news_article_serializer.data, status=request_status)

        except (EmptyResultSet, NewsArticle.DoesNotExist):

            try:
                news_article_query = NewsURLContent.objects.get(create_query_news_content(news))
                data = {
                    "news_article": news_article_query.article_content,
                    "model_prediction": news_article_query.model_prediction,
                    "model_probability": news_article_query.model_probability,
                    "date_reported": news_article_query.url.date_reported,
                    "article_valid": news_article_query.url.url_valid,
                    "date_checked": news_article_query.url.date_checked
                }

                news_article_serializer = NewsArticleSerializer(NewsArticle(**data))
                request_status = status.HTTP_206_PARTIAL_CONTENT if news_article_query.url.url_valid is None else status.HTTP_200_OK
                return Response(data=news_article_serializer.data, status=request_status)

            except (EmptyResultSet, NewsURLContent.DoesNotExist):
                try:
                    pred, prob = fetch_fakescore(news)
                    prob = convert_fakescore(pred, prob)
                except ServiceTemporaryUnavailable:
                    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

            data = {
                    "news_article": news,
                    "model_prediction": pred,
                    "model_probability": prob
                    }

            news_article_serializer = NewsArticleSerializer(NewsArticle(**data))

            return Response(data=news_article_serializer.data, status=status.HTTP_202_ACCEPTED)


class ArticleReportAPI(APIView):

    permission_classes = [AllowAny]

    @staticmethod
    def get(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def post(request):
        try:
            news = request.data["news_article"]
            pred = request.data["model_prediction"]
            prob = request.data["model_probability"]

        except KeyError:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
                "news_article": news,
                "model_prediction": pred,
                "model_probability": prob
                }

        article = NewsArticle(**data)

        article.save()
        return Response(status=status.HTTP_201_CREATED)
