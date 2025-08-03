from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
from django.views import View
from .forms import TagListForm
from .models import Tag, Offer, Application, Report
from authentication.models import User

from dashboard.models import Bookmark

from .tasks import send_report_notification

# Create your views here.

class SearchView(View):

    template_name = "jobs/search.html"

    def get(self, request):
        # skip filtering logic for now
        tags_list = Tag.objects.all()
        offer_list = Offer.objects.all()
        context = {
            'tags_list': tags_list,
            'offer_list': offer_list,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        tags_list = request.POST.getlist('tags')
        tags = Tag.objects.filter(id__in=tags_list)
        print(tags)
        print(request.POST)
    

class JobDetailsView(View):

    template_name = "jobs/components/job_details.html"

    def get(self, request, offer_id:int):

        offer = Offer.objects.get(id=offer_id)
        bookmarked = offer.bookmark_set.filter(bookmarked_by = request.user).exists()
        applied = Application.objects.filter(applicant = request.user, position = offer).exists()
        reported = Report.objects.filter(reported_by = request.user, offer = offer).exists()

        context = {
            'index': offer_id,
            'job': offer,
            'bookmarked': bookmarked,
            'applied': applied,
            'reported': reported,
        }
        return render(request, self.template_name, context=context)
    

class BookamrkOfferView(View):

    def post(self, request, offer_id : int):

        offer = get_object_or_404(Offer, id=offer_id)
        user = get_object_or_404(User, email = request.user)
        if Bookmark.objects.filter(bookmarked_offer = offer, bookmarked_by = user).exists():
            #the offer is already bookmarked
            return HttpResponse(content = "Theoffer is bookmarked")
        
        bookmark = Bookmark.objects.create(bookmarked_offer = offer, bookmarked_by = user)
        bookmark.save()
        return HttpResponse(content = "Kinda worked or not really...")
    

class ReportOfferModal(View):
    def get(self, request, offer_id:int):

        context = {
            "job": {
                "id": offer_id,
            }
        }
        return render(request, 'jobs/components/report_modal.html', context=context)
    
    def post(self, request, offer_id:int):
        offer = get_object_or_404(Offer, id = offer_id)

        if  Report.objects.filter(reported_by = request.user, offer = offer).exists():
            #already reported - no actions
            return HttpResponse(content="Offer already reported!")
        report = Report.objects.create(reported_by = request.user, offer = offer)
        if report is not None:
            report.save()
            send_report_notification("Report notification: Job Offer Report - {}".format(offer_id), "A job has been reported. Investigation pending.", settings.RECIPIENT_ADDRESS)
        return HttpResponse(content="Offer has been reported")

