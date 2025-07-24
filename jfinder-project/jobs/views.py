from django.shortcuts import render
from django.views import View
from .forms import TagListForm
from .models import Tag

# Create your views here.

class SearchView(View):

    template_name = "jobs/search.html"

    def get(self, request):
        # skip filtering logic for now
        tags_list = Tag.objects.all()
        context = {
            'tags_list': tags_list,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        tags_list = request.POST.getlist('tags')
        tags = Tag.objects.filter(id__in=tags_list)
        print(tags)
        print(request.POST)
    

class JobDetailsView(View):

    template_name = "jobs/components/job_details.html"

    def get(self, request, index:str):
        context = {
            "job": {
                "index": index,
            }
        }
        return render(request, self.template_name, context=context)