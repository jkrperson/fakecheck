from rest_framework import serializers
from .models import ThreatDomain, NewsArticle, NewsURL, NewsURLContent


class ThreatDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatDomain
        fields = '__all__'


class NewsUrlSerializer(serializers.ModelSerializer):

    domain = ThreatDomainSerializer

    class Meta:
        model = NewsURL
        fields = ("news_url", "domain", "date_reported", "url_valid", "date_checked")

    def create(self, validated_data):
        newsurl = NewsURL.objects.create(**validated_data)
        return newsurl


class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'


class NewsUrlContentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsURLContent
        fields = "__all__"


class NewsUrlContentSerializer(serializers.Serializer):
    url = NewsUrlSerializer(required=True)
    article_content = serializers.CharField()
    model_prediction = serializers.CharField(max_length=5)
    model_probability = serializers.FloatField()


class NewsArticleContentSerializer(serializers.Serializer):
    news_article = serializers.CharField()
    model_prediction = serializers.CharField(max_length=5)
    model_probability = serializers.FloatField()

