from django.db import models

# Create your models here.
# TODO:
# Create:   -model for news article storage (For admin checking)
#           -model for news url storage (For admin checking)
#           -model for verified news article/url storage


class ThreatDomain(models.Model):
    domain = models.URLField(unique=True)
    fakenews_num = models.IntegerField(default=0)
    realnews_num = models.IntegerField(default=0)

    def __str__(self):
        return self.domain


class NewsURL(models.Model):
    news_url = models.URLField(unique=True)
    domain = models.ForeignKey(ThreatDomain, on_delete=models.SET_NULL, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    url_valid = models.BooleanField(null=True)
    date_checked = models.DateTimeField(null=True)
    # verifier = models.ForeignKey()


class NewsURLContent(models.Model):
    url = models.OneToOneField(NewsURL, on_delete=models.CASCADE)
    article_content = models.TextField(blank=True, null=True)
    model_prediction = models.CharField(max_length=5, blank=True, null=True)
    model_probability = models.FloatField(blank=True, null=True)


class NewsArticle(models.Model):
    news_article = models.TextField()
    model_prediction = models.CharField(max_length=5, blank=True, null=True)
    model_probability = models.FloatField(blank=True, null=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    article_valid = models.BooleanField(blank=True, null=True)
    date_checked = models.DateTimeField(blank=True, null=True)
    # verifier = models.ForeignKey()

