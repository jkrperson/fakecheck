from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.http.response import HttpResponse

# Serve Single Page Application
index = never_cache(TemplateView.as_view(template_name='index.html'))


def example(request):
    text_example = """MAYNILA—Pinalaya na ang 11 pang trabahador ng Regent Foods Corporation na ikinulong sa Pasig City.
    Ayon sa grupong Defend Job Philippines, pinalaya ang mga trabahador matapos makumpleto ang perang pang piyansa na inutang sa mga kamag-anak at kaibigan.
    Inaresto ang kabuuang 23 katao, kabilang ang 20 trabahador ng Regent, 2 miyembro ng labor organization at 1 tricycle driver matapos ang isinagawang rally noong Nobyembre 9.
    Una na ring hiniling ni Pasig City Mayor Vico Sotto sa pamunuan ng Regent Foods Corporation na huwag nang ituloy ang kaso.
    Gayunpaman, ayon kay Mark Piad, legal counsel ng Regent, na magtitiwala ang kompanya sa legal at judicial process kaugnay sa kaso ng tinaguriang Regent 23."""

    filename = "example.txt"
    response = HttpResponse(text_example, content_type='text/plain')
    response["Content-Disposition"] = 'attachment; filename={0}'.format(filename)
    return response

