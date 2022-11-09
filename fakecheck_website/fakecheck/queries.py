from difflib import SequenceMatcher

from django.db.models import Q
from django.core.exceptions import EmptyResultSet

from fakecheck.models import NewsArticle, NewsURLContent


def create_query_article(fulltext):
    # TODO: Optimize query function
    article_content = NewsArticle.objects.values_list('pk', 'news_article')
    if article_content:
        for article in article_content:
            score = SequenceMatcher(None, fulltext, article[1]).ratio()
            if score >= 0.90:
                return Q(pk=article[0])
        raise NewsArticle.DoesNotExist
    raise EmptyResultSet


def create_query_news_content(fulltext):
    article_content = NewsURLContent.objects.values_list('pk', 'article_content')
    if article_content:
        for article in article_content:
            score = SequenceMatcher(None, fulltext, article[1]).ratio()
            if score >= 0.90:
                return Q(pk=article[0])
        raise NewsURLContent.DoesNotExist
    raise EmptyResultSet
