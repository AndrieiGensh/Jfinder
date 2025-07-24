from django.shortcuts import render,HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views import View
from django.views.generic import DetailView

from django.conf import settings
from django.template.loader import render_to_string

from weasyprint import HTML, CSS
import json
from  datetime import datetime
import jinja2



import functools

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher

import ssl

class MyDetailView(DetailView):
    # vanilla Django DetailView
    template_name = 'cvbuilder/cv_templates/index_template.html'

def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    cloud_storage_url = 'https://s3.amazonaws.com/django-weasyprint/static/'
    if url.startswith(cloud_storage_url):
        url = 'file://' + url.replace(cloud_storage_url, settings.STATIC_URL)
    return django_url_fetcher(url, *args, **kwargs)

class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to pass a kwarg to URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(custom_url_fetcher, ssl_context=context)

class PrintView(WeasyTemplateResponseMixin, MyDetailView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        settings.BASE_DIR / 'static' / 'css/output.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

    def get(self, request):
        return self.response_class(request, )


EXP_DATA = {
    'personal': {
        'name': {
            'first': 'Andras',
            'second': 'Gens',
        },
        'contact': {
            'email': 'email@gmail.com',
            'phone': +345869484,
        },
        'location': {
            'country': 'Poland',
            'city': 'City',
        },
    },
    'education': [
        {
            'institution': 'Univerity',
            'subject': 'Subject',
            'degree': 'Degree',
            'GPA': 5.6,
            'description': 'Studies description goes here',
            'start_date': 'Date here',
            'end_date': 'Date here',
        },
        {
            'institution': 'Univerity',
            'subject': 'Subject',
            'degree': 'Degree',
            'GPA': 5.6,
            'description': 'Studies description goes here',
            'start_date': 'Date here',
            'end_date': 'Date here',
        },
    ],
    'work_experience': [
        {
            'employer': 'Employer',
            'potision': 'Position description goes here',
            'description': 'Responsibilities go here',
            'start_date': 'Date here',
            'end_date': 'Date here',
        },
        {
            'employer': 'Employer',
            'potision': 'Position description goes here',
            'description': 'Responsibilities go here',
            'start_date': 'Date here',
            'end_date': 'Date here',
        }
    ],
    'certificates': [
        {
            'name': 'Cert name',
            'start_date': 'Date here',
            'end_date': 'Date here',
        },
        {
            'name': 'Cert name',
            'start_date': 'Date here',
            'end_date': 'Date here',
        },
    ],
    'skills': {
        'soft': [
            {
                'name': 'name of the skill'
            },
            {
                'name': 'name of the skill'
            },
            {
                'name': 'name of the skill'
            },
        ],
        'hard': [
            {
                'name': 'name of the skill'
            },
            {
                'name': 'name of the skill'
            },
            {
                'name': 'name of the skill'
            },
        ]
    },
    'tools': [
        {
            'name': 'Tool or other technology',
        },
        {
            'name': 'Other tool or other technology',
        },
        {
            'name': 'Tool',
        },
    ],
    'projects': [
        {
            'name': 'Acrada',
            'link': 'url/url/html',
            'description': 'Lorem ipsum dolot sit amet'
        },
        {
            'name': 'Non Arcada',
            'link': 'url/url/html',
            'description': 'Lorem ipsum dolot sit amet'
        },
    ],
    'languages': [
        {
            'name': 'Polish',
            'proficiency': {
                'text': 'Advanced',
                'value': 4,
            }
        },
        {
            'name': 'English',
            'proficiency': {
                'text': 'Intermediate',
                'value': 3,
            }
        }
    ],
    'statement': {
        'display': True,
        'text': "",
    },
}

# Create your views here.

def pdf_generation_test(template_path, context):
    # environment = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=settings.BASE_DIR / 'templates/cvbuilder/cv_templates'), autoescape=True)
    # environment.globals.update({
    #     'static': staticfiles_storage.url,
    # })
    # try:
    #     template = environment.get_template(template_path)
    # except Exception as e:
    #     print(e)
    template = render_to_string(template_name=template_path, context=context)
    return template

from django_weasyprint.utils import django_url_fetcher
import logging
logger = logging.getLogger('weasyprint')
module_logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('debug.log'))
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(message)s"))
module_logger.addHandler(ch)
# stylesheets = [CSS(url='file://' + settings.STATIC_URL + 'css/output.css', base_url="file://", url_fetcher=django_url_fetcher)]

class CVBuilderView(View):

    def get(self, request):
        # # html = HTML(string = pdf_generation_test('index_template.html', { 'data': EXP_DATA}))
        # # css_path = [
        # #     '././static/css/output.css',
        # # ]
        # css = CSS(settings.BASE_DIR / 'static/css/output.css',)
        # # print(css.base_url)
        # # print(settings.BASE_DIR / 'static/css/output.css')
        # html = HTML(string = render_to_string('cvbuilder/cv_templates/index_template.html', { 'data': EXP_DATA}), base_url="file://", url_fetcher=django_url_fetcher)
        # name = f"output-{datetime.now().date()}"
        # filename = f"{name}.pdf"
        # pdf_file = html.write_pdf(filename, media_type="screen")
        return HttpResponse(render_to_string('cvbuilder/builder.html', { 'data': EXP_DATA}))
        # return render(request, 'cvbuilder/builder.html', context={})

    def post(self, request):
        return
