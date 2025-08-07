from django.shortcuts import render,HttpResponse
from django.views import View

import jinja2
from jinja2 import Environment, FileSystemLoader

from pathlib import Path

import os

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

class CVBuilderView(View):

    def get(self, request):

        base_path = os.path.join(Path(__file__).resolve().parent.parent, 'templates/cvbuilder/cv_templates')
        dist_dir = 'dist'
        dist_path = os.path.join(base_path, dist_dir)

        print(base_path, dist_path)


        jinja_env = Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=FileSystemLoader(searchpath = base_path),
        )

        template = jinja_env.get_template('template.tex')
        template_out_path = os.path.join(dist_path, 'template_output.tex')

        with open(template_out_path, 'w') as fout:
            fout.write(template.render(resume = {
                'name' : 'Andras',
                'contact': {
                    'phone': 1234567,
                    'email': 'test@gmail.com',
                    'linkedin': 'https://something/here'
                },
                'summary': {
                    "one": 'one',
                    'two': 'two',
                    'three': 'three',
                }
            }))

        os.system('pdflatex -interaction=nonstopmode -output-directory={} {}'.format(dist_path, template_out_path))

        return render(request, 'cvbuilder/builder.html', context={})

    def post(self, request):
        return
