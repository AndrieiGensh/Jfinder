from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

import jinja2
from jinja2 import Environment, FileSystemLoader

from pathlib import Path

import os

from .models import ResumeCreationSessionModel
from .forms import CVForm
from .tasks import generate_cv

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

class CVBuilderMenuView(View):

    template = 'cvbuilder/menu.html'

    def get(self, request):

        sessions = ResumeCreationSessionModel.objects.filter(user = request.user).all()

        context = {
            "sessions": sessions,
        }

        return render(request, self.template, context = context)

    def post(self, request):
        return


class CVBuilderTemplatePreview(View):

    template = 'cvbuilder/components/template_preview.html'

    def get(self, request):
        return render(request, self.template, {})


    def post(self, request):
        pass


class CVBuilderEditorView(View):

    template = "cvbuilder/editor.html"

    def get(self, request):
        session_id = request.GET.get("editor_session")
        if not session_id:
            session = ResumeCreationSessionModel(user = request.user)
            session.save()

            print("session:", session.id)

            return redirect(reverse("cvbuilder_editor", query = {"editor_session": session.pk}))

        else:
            session = ResumeCreationSessionModel.objects.get(user = request.user, id = session_id)
            context = {
                "settings": session.settings,
                "template": session.template,
                "content": session.content_config,
            }
        # check for the session. There always should be one associated with the id - an identifier of the document so to speak thet the user works on. 
        # If there is none - it means that the session is for a new doc.
        # Get the session (old or new). Populate the form with data from the session.
        # Serve the template with the redirect to the same url but with pushed session id as a param (for the future post requests)
            print(session.content_config)
            return render(request, self.template, context=context)
        
    def post(self, request):
        pass