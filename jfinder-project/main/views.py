from django.shortcuts import render
from django.views import View

# Create your views here.

class ProfileView(View):

    template_name = "main/profile.html"

    def get(self, request):
        return render(request, self.template_name, context = {})
    

class IndexView(View):

    template_name = "main/index.html"

    def get(self, request):
        return render(request, self.template_name, context={})
