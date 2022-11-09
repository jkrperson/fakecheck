import requests
from urllib.parse import urlparse
from html.parser import HTMLParser
from readability import Document
from readability.cleaners import normalize_spaces



from fakecheck.errors import SiteNotFound, ServiceTemporaryUnavailable


def fetch_fakescore(news):
    """
    Inputs the news string and returns fakescore
    :param news:
    :return prediction, probability:
    """
    url = "https://celt-fakenews.herokuapp.com/predict"

    resp_non = requests.post(url, json={"news": news})
    status = resp_non.status_code
    if status != 200:
        raise ServiceTemporaryUnavailable
    resp = resp_non.json()
    return resp['prediction'], resp['prob']


def convert_fakescore(pred, prob):
    """
    Inputs the prediction and probability and converts it in order to make it better???
    :param pred:
    :param prob:
    :return modified probability:
    """
    if pred == "REAL":
        return 100-prob
    else:
        return prob


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def retrieve_article_content(url):
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"

    headers = {'User-Agent': agent}

    response = requests.get(url=url, headers=headers)

    if response.status_code == 404:
        raise SiteNotFound

    doc = Document(response.text)
    article = doc.summary()
    return strip_tags(normalize_spaces(article)).strip()


def get_domain(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
