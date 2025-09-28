from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

import jinja2
from jinja2 import Environment, FileSystemLoader

from pathlib import Path

import uuid
import os

from .models import ResumeCreationSessionModel
from .tasks import generate_cv
from .utils import CVBuilderEntityFormFactory
from jfinder.utils import MessageAction, MessageContext

from main.models import Document

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
            file = Document.objects.all()
            context = {
                "settings": session.settings,
                "template": session.template,
                "content": session.content_config,
                "file": file[2],
            }
        # check for the session. There always should be one associated with the id - an identifier of the document so to speak thet the user works on. 
        # If there is none - it means that the session is for a new doc.
        # Get the session (old or new). Populate the form with data from the session.
        # Serve the template with the redirect to the same url but with pushed session id as a param (for the future post requests)
            print(session.content_config)
            request.session["editor_session_id"] = session.id
            return render(request, self.template, context=context)
        
    def post(self, request):
        pass


class CVBuilderEditorCreateEntity(View):

    form_factory = CVBuilderEntityFormFactory()
    template = 'cvbuilder/components/editor_form.html'

    def get(self, request):
        print("Requested create entity form")
        entity_type = request.GET.get("entity_type")
        if not entity_type:
            print("Woops, no entity type")
            return "Woops, no entity type"
        form = self.form_factory.get_form(entity_type)
        if not form:
            print("Woops, no such form for this entity type")
            return "Woops, no such form for this entity type"
        context = {
            "form": form(),
            "entity_type": entity_type,
            "swap_oob": True,
            "action": "create",
        }
        return render(request, self.template, context=context)

    def post(self, request):
        session_id = request.session.get("editor_session_id")
        if not session_id:
            redirect(reverse("cvbuilder_menu"))
        else:
            session = ResumeCreationSessionModel.objects.get(id=session_id, user=request.user)
            if not session:
                redirect(reverse("cvbuilder_menu"))
            else:
                entity_type = request.POST.get("entity_type")
                form = self.form_factory.get_form(entity_type)(request.POST)
                if not form:
                    print("No for for ", entity_type)
                    print(request.POST)
                    message = MessageContext(type="error", message="Wrong entitytype. No such form", action= MessageAction())
                    context = {
                        "message": message,
                    }
                    return render(request, "main/components/dialog_message.html", context = context)
                else:
                    if form.is_valid():
                        new_id = uuid.uuid4()
                        session.content_config[entity_type]["data"][str(new_id)] = {
                            "show": True,
                            "data": form.cleaned_data,
                        }
                        session.save(update_fields=["content_config"])
                        context = {
                            "settings": session.settings,
                            "template": session.template,
                            "content": session.content_config,
                            "swap_oob": True,
                        }
                        return render(request, "cvbuilder/components/editor_sections_container.html", context = context)


class CVBuilderEditorDeleteEntity(View):

    template = 'cvbuilder/components/editor_sections_container.html'

    def get(self, request):
        pass

    def post(self, request):
        session_id = request.POST.get("editor_session")
        user = request.user
        if not session_id:
            return None # return error message
        else:
            session = get_object_or_404(ResumeCreationSessionModel, id=session_id, user = user)
            if session:
                key = request.POST.get("content_key")
                record_id = request.POST.get("record_id")

                if not key or not record_id:
                    return None # return error or redirect
                else:
                    session.content_config[key].pop(record_id, None)
                    session.save(update_fields=["content_config"])

                    context = {
                        "settings": session.settings,
                        "template": session.template,
                        "content": session.content_config,
                        "swap_oob": True,
                    }

                    return render(request, self.template, context = context)
            else:
                return None # return error message or redirect to editor preview


class CVBuilderEditorEditEntity(View):

    form_factory = CVBuilderEntityFormFactory()
    template = 'cvbuilder/components/editor_form.html'

    def get(self, request):
        print("Requested edit entity form")
        session_id = request.session.get("editor_session_id")
        if not session_id:
            redirect(reverse("cvbuilder_menu"))
        else:
            session = ResumeCreationSessionModel.objects.get(id=session_id, user=request.user)
            if not session:
                redirect(reverse("cvbuilder_menu"))
            else:
                entity_type = request.GET.get("entity_type")
                record_id = request.GET.get("record_id")
                form = self.form_factory.get_form(entity_type)
                if not form or not (entity_type or record_id):
                    print("No form for ", entity_type)
                    print(request.GET)
                    message = MessageContext(type="error", message="No form for provided parameters", action= MessageAction())
                    context = {
                        "message": message,
                    }
                    return render(request, "main/components/dialog_message.html", context = context)
                else:
                    context = {
                        "form": form(session.content_config[entity_type]["data"][record_id]["data"]),
                        "entity_type": entity_type,
                        "record_id": record_id,
                        "swap_oob": True,
                        "action": "edit",
                    }
                    return render(request, self.template, context=context)

    def post(self, request):
        print("Requested edit entity form")
        session_id = request.session.get("editor_session_id")
        if not session_id:
            redirect(reverse("cvbuilder_menu"))
        else:
            session = ResumeCreationSessionModel.objects.get(id=session_id, user=request.user)
            if not session:
                redirect(reverse("cvbuilder_menu"))
            else:
                entity_type = request.POST.get("entity_type")
                record_id = request.POST.get("record_id")
                form = self.form_factory.get_form(entity_type)
                if not form or not (entity_type or record_id):
                    print("No form for ", entity_type)
                    print(request.POST)
                    message = MessageContext(type="error", message="No form for provided parameters", action= MessageAction())
                    context = {
                        "message": message,
                    }
                    return render(request, "main/components/dialog_message.html", context = context)
                else:
                    form = form(request.POST)
                    if form.is_valid():
                        session.content_config[entity_type]["data"][record_id]["data"] = form.cleaned_data
                        session.save(update_fields=["content_config"])
                        context = {
                            "settings": session.settings,
                            "template": session.template,
                            "content": session.content_config,
                            "swap_oob": True,
                        }
                        return render(request, "cvbuilder/components/editor_sections_container.html", context = context)
                    else:
                        message = MessageContext(
                            type="error",
                            message="Form is invalid",
                            action=MessageAction()
                        )
                        context = {
                            "message": message,
                        }
                        return render(request, "main/components/dialog_message.html", context = context)


class CVBuilderEditorSectionsContainer(View):

    template = "cvbuilder/components/editor_sections_container.html"

    def get(self, request):

        session_id = request.session.get("editor_session_id")
        if not session_id:
            print("Hmm no id")
            redirect(reverse("cvbuilder_menu"))
        else:
            print("ID provided")
            session = ResumeCreationSessionModel.objects.get(user = request.user, id = session_id)
            context = {
                "settings": session.settings,
                "template": session.template,
                "content": session.content_config,
            }
            return render(request, self.template, context = context)
