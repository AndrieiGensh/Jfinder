from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.template.loader import render_to_string
from authentication.models import User
from main.models import UserProfile, Document, Education, Experience
from main.forms import EducationForm, ExperienceForm

# Create your views here.

class ProfileView(View):

    template_name = "main/profile.html"

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            "profile": user_profile,
        }
        return render(request, self.template_name, context = context)

class EducationCreateView(View):

    education_form = EducationForm

    education_modal = 'main/components/education_modal.html'
    education_table = 'main/components/education_table.html'

    def get(self, request):
        form = self.education_form()
        context = {
            'form': form,
        }
        return render(request, self.education_modal, context=context)
    
    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = self.education_form(request.POST)
        if form.is_valid():
            print("valid form edu")
            education_instance = form.save(commit=False)
            education_instance.profile = user_profile
            education_instance.save()

            education_list = Education.objects.filter(profile = user_profile).all()
            context = {
                "education_list": education_list,
                "swap_oob": True,
            }
            html = render_to_string(self.education_table, context = context, request = request)
            response = HttpResponse(html)
            response.headers["HX-Trigger"] = '{"closeModal":true}'
            return response
        print(form, form.errors)
        

class ExperienceCreateView(View):

    experience_form = ExperienceForm

    experience_modal = 'main/components/experience_modal.html'
    experience_table = 'main/components/experience_table.html'

    def get(self, request):
        form = self.experience_form()
        context = {
            'form': form,
        }
        return render(request, self.experience_modal, context=context)
    
    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = self.experience_form(request.POST)
        if form.is_valid():
            print("valid form exp")
            experience_instance = form.save(commit=False)
            experience_instance.profile = user_profile
            experience_instance.save()

            experience_list = Experience.objects.filter(profile = user_profile).all()
            context = {
                "experience_list": experience_list,
                "swap_oob": True,
            }
            html = render_to_string(self.experience_table, context = context, request = request)
            response = HttpResponse(html)
            response.headers["HX-Trigger"] = '{"closeModal":true}'
            return response


class DocumentView(View):

    def get(self, request, index:int):
        document = get_object_or_404(Document, id=index, uploader = request.user)
        # research how to supply files from backend efficiently
        pass
    

class IndexView(View):

    template_name = "main/index.html"

    def get(self, request):
        return render(request, self.template_name, context={})
