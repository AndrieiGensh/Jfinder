from django.shortcuts import render, get_object_or_404, HttpResponse
from django.conf import settings
from django.views import View
from django.db.models import Q
from .forms import TagListForm
from .models import Tag, Offer, Application, Report
from authentication.models import User

from dashboard.models import Bookmark

from .tasks import send_report_notification

# Create your views here.

class SearchView(View):

    template = "jobs/search.html"
    partial_job_list = "jobs/components/job_list.html"
    nothing_found = "jobs/components/job_list_empty.html"

    def get(self, request):
        # get query parameters from get and do the filtering
        keyword = request.GET.get("search_keyword")
        country = request.GET.get('country')
        city = request.GET.get("city")
        work_mode = request.GET.get("work_mode")
        salary_mode = request.GET.get("salary_mode")
        min_salary = request.GET.get("min_salary")
        max_salary = request.GET.get("max_salary")
        tag_slugs = request.GET.getlist("tags")
        benefit_slugs = request.GET.getlist("benefits")

        offer_list = Offer.objects.all()

        if keyword:
            offer_list = offer_list.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(requirements__icontains=keyword) |
                Q(nice_to_have__icontains=keyword)
            )
        print(keyword)
        if country:
            offer_list = offer_list.filter(
                location_country=country
            )
        if city:
            offer_list = offer_list.filter(
                location_city=city
            )
        if work_mode:
            offer_list = offer_list.filter(
                work_mode=work_mode
            )
        if salary_mode:
            offer_list = offer_list.filter(
                salary_mode = salary_mode
            )
        if min_salary:
            offer_list = offer_list.filter(
                min_salary=min_salary
            )
        if max_salary:
            offer_list = offer_list.filter(
                max_salary=max_salary
            )
        if tag_slugs:
            offer_list = offer_list.filter(
                tags_slug__contains=tag_slugs
            )
        if benefit_slugs:
            offer_list = offer_list.filter(
                benefits_slug__contains=benefit_slugs
            )

        context = {
            'tag_list': [],
            'offer_list': offer_list,
        }

        tag_list = Tag.objects.all()
        tag_list_with_selected = [
            {
                "data": tag,
                "selected": tag.slug in tag_slugs,
            } for tag in tag_list
        ]
        context['tag_list'] = tag_list_with_selected
        # check if the request is HTMX or not
        if request.htmx:
            # retun only the partial, populated with filterred job offers
            if offer_list.count() == 0:
                return render(request, self.nothing_found, context = {})
            else:
                # or an nothing_found partial with there is nothing to display
                return render(request, self.partial_job_list, context=context)
        else:
            # else return the whole template with the partial included
            return render(request, self.template, context=context)
    
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
            return HttpResponse(content = "The offer is bookmarked")
        
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

