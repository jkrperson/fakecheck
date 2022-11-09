import time
from csv import reader, writer
from difflib import SequenceMatcher

from django.test import TestCase
from django.urls import reverse

from fakecheck.data_fetching import fetch_fakescore, convert_fakescore
from fakecheck.errors import ServiceTemporaryUnavailable

from rest_framework import status
from rest_framework.test import APITestCase

from fakecheck.models import ThreatDomain, NewsURL, NewsArticle

# Input your tests here


class CheckURLAPITestCases(APITestCase):

    def setUp(self):
        self.url = reverse("URLCheckAPI")
        self.news_csv_file = open('fakecheck/test_csv/news.csv', "r")
        self.time_results_csv_file = open('fakecheck/result_csv/URL_news_check_time.csv', "w")

    def test_check_news_time(self):
        csv_reader = reader(self.news_csv_file, delimiter="|", quotechar="$")
        result_csv_writer = writer(self.time_results_csv_file, delimiter="|")
        result_csv_writer.writerow(["News #", "Total time Spent (s)", "# of Trials", "# of Characters", "Similarity to real article"])
        for row in csv_reader:

            if int(row[0]) > 0:
                print(row[0])
                data = {"news_url": row[1]}
                status_number = 503
                response = None
                trials = 0
                tot_time = 0
                while status_number == 503:

                    trials += 1

                    # Time recording start
                    start_time = time.time()

                    response = self.client.post(self.url, data, format="json")

                    # Time recording stop
                    stop_time = time.time()

                    status_number = response.status_code
                    print(status_number)
                    tot_time += stop_time-start_time

                # Record response
                result_csv_writer.writerow([row[0], tot_time, trials, len(response.json()["article_content"]), SequenceMatcher(None, response.json()["article_content"], row[2]).ratio()])

    def tearDown(self):

        self.news_csv_file.close()
        self.time_results_csv_file.close()


class ReportingURLAPITestCases(APITestCase):

    def setUp(self):
        self.check_url = reverse("URLCheckAPI")
        self.report_url = reverse("URLReportAPI")
        self.news_csv_file = open('fakecheck/test_csv/news.csv', "r")
        self.time_results_csv_file = open('fakecheck/result_csv/URL_report_news_time.csv', "w")

    def test_report_news_time(self):
        csv_reader = reader(self.news_csv_file, delimiter="|", quotechar="$")
        result_csv_writer = writer(self.time_results_csv_file, delimiter="|")
        result_csv_writer.writerow(["News #", "Total time Spent (s)"])
        for row in csv_reader:

            if int(row[0]) > 0:
                print(row[0])
                data = {"news_url": row[1]}
                status_number = 503
                response = None
                while status_number == 503:

                    response = self.client.post(self.check_url, data, format="json")
                    status_number = response.status_code

                # Time recording start
                start_time = time.time()
                response = self.client.post(self.report_url, response.json(), format="json")
                # Time recording stop
                stop_time = time.time()

                # Record response
                result_csv_writer.writerow([row[0], stop_time-start_time])

    def tearDown(self):

        self.news_csv_file.close()
        self.time_results_csv_file.close()


class ReportCheckURLAPITestCase(APITestCase):

    def setUp(self):
        self.check_url = reverse("URLCheckAPI")
        self.report_url = reverse("URLReportAPI")
        self.news_csv_file = open('fakecheck/test_csv/news.csv', "r")
        self.time_results_csv_file = open('fakecheck/result_csv/URL_report_check_news_time.csv', "w")

    def test_report_check_news_time(self):
        csv_reader = reader(self.news_csv_file, delimiter="|", quotechar="$")
        result_csv_writer = writer(self.time_results_csv_file, delimiter="|")
        result_csv_writer.writerow(["News #", "Total time Spent (s)"])
        for row in csv_reader:

            if int(row[0]) > 0:
                print(row[0])
                data = {"news_url": row[1]}
                status_number = 503
                response = None
                while status_number == 503:
                    response = self.client.post(self.check_url, data, format="json")
                    status_number = response.status_code

                response = self.client.post(self.report_url, response.json(), format="json")

        csv_reader = reader(self.news_csv_file, delimiter="|", quotechar="$")

        for row in csv_reader:
            if int(row[0]) > 0:
                print(row[0])
                data = {"news_url": row[1]}
                status_number = 503
                response = None
                while status_number == 503:
                    # Time recording start
                    start_time = time.time()

                    response = self.client.post(self.check_url, data, format="json")

                    # Time recording stop
                    stop_time = time.time()

                    # Record response
                    result_csv_writer.writerow([row[0], stop_time - start_time])

                    status_number = response.status_code

    def tearDown(self):

        self.news_csv_file.close()
        self.time_results_csv_file.close()


class CheckArticleAPITestCase(APITestCase):

    def setUp(self):
        self.check_article = reverse("ArticleCheckAPI")
        self.news_csv_file = open('fakecheck/test_csv/news.csv', "r")
        self.time_results_csv_file = open('fakecheck/result_csv/Article_check_news_time.csv', "w")

    def test_check_article_accuracy(self):
        csv_reader = reader(self.news_csv_file, delimiter="|", quotechar="$")
        result_csv_writer = writer(self.time_results_csv_file, delimiter="|")
        result_csv_writer.writerow(["News #", "Total time Spent (s)", "Trials", "Difference from non-API fake score", "Errors" ])
        for row in csv_reader:
            if int(row[0]) > 0:
                print(row[0])

                data = {"news_article": row[2]}

                status_number1 = 503
                status_number2 = 503
                response1 = None
                response2 = None
                time_tot = 0
                trials = 0
                while status_number1 == 503:

                    trials += 1
                    start_time = time.time()

                    response1 = self.client.post(self.check_article, data=data, format="json")

                    time_tot += time.time() - start_time

                    status_number1 = response1.status_code

                while status_number2 == 503:
                    try:
                        response2 = fetch_fakescore(row[2])
                        response2 = (response2[0], convert_fakescore(response2[0], response2[1]))
                        status_number2 = 200
                    except ServiceTemporaryUnavailable:
                        pass

                response1 = response1.json()

                error_message = ""
                if response2[0] == "REAL" and response2[0] != response1['model_prediction']:
                    error_message = "False Negative"
                elif response2[0] == "FAKE" and response2[0] != response1['model_prediction']:
                    error_message = "False Positive"
                else:
                    error_message = "No Error"

                result_csv_writer.writerow([row[0], time_tot, trials, abs(response1["model_probability"] - response2[1]), error_message])

    def tearDown(self):

        self.news_csv_file.close()
        self.time_results_csv_file.close()
