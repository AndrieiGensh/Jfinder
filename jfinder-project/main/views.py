from django.shortcuts import render, get_object_or_404
from django.views import View
from authentication.models import User
from main.models import UserProfile

# Create your views here.

class ProfileView(View):

    template_name = "main/profile.html"

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            "profile": user_profile,
        }
        return render(request, self.template_name, context = context)
    

class IndexView(View):

    template_name = "main/index.html"

    def get(self, request):
        return render(request, self.template_name, context={})
