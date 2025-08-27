from django.shortcuts import render, get_object_or_404, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views import View
from django.db.models import Q
from .forms import TagListForm
from .models import Tag, Offer, Application, Report
from authentication.models import User

from dashboard.models import Bookmark
from main.models import Document
from main.forms import DocumentForm

from jfinder.utils import MessageContext, MessageAction

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
        bookmarked = Bookmark.objects.filter(bookmarked_by = request.user, bookmarked_offer = offer).exists()
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
    

class ApplicationCreateModal(View):

    application_modal = "jobs/components/application_modal.html"
    application_message = "main/components/dialog_message.html"
    application_error = "jobs/components/application_error.html"

    upload_file_form = DocumentForm

    def get(self, request, id: int):
        offer = get_object_or_404(Offer, id=id)
        if Application.objects.filter(
            applicant = request.user,
            position = offer
        ).exists():
            # aplready applied for the position.
            message = MessageContext(
                type="warning",
                message="Already applied for this offer",
                action=MessageAction()
            )
            context = {
                "message": message.as_context(),
            }
            return render(request, self.application_message, context=context)
        context = {
            "job": {
                "id": id,
            }
        }
        return render(request, self.application_modal, context = context)


    def post(self, request, id: int):
        from main.models import FileSourceTypeChoices
        offer = get_object_or_404(Offer, id=id)
        #TODO:
        # improve logic here: check for the most recent application date and the status
        # should be possible to re-apply if status is anything other than success or pending
        # or if the date of last application is before the 'from' date on the offer

        if Application.objects.filter(
            applicant = request.user,
            position = offer
        ).exists():
            print("Application exists")
            # very unlikely since I am bloking the access to the button, but still, good to have
            message = MessageContext(
                type="warning",
                message="Already applied for this offer",
                action=MessageAction()
            )
            context = {
                "message": message.as_context(),
            }
            html = render_to_string(self.application_message, context = context, request = request)
            response = HttpResponse(html)
            response.headers["HX-Trigger"] = '{"closeModal":true}'
            return response
        else:
            # if applying with internal file
            print("checking for the internal file submition")
            document_id = request.POST.get("internal_cv")
            if document_id:
                print("is internal")
                document = get_object_or_404(Document, id = document_id, uploader = request.user, source_type = FileSourceTypeChoices.INTERNAL)
                application = Application.objects.create(applicant = request.user, position = offer, supplied_cv = document)
                application.save()
                message = MessageContext(
                    type="success",
                    message="Applied successfully",
                    action=MessageAction()
                )
                context = {
                    "message": message.as_context(),
                }
                html = render_to_string(self.application_message, context = context, request = request)
                response = HttpResponse(html)
                response.headers["HX-Trigger"] = '{"closeModal":true}'
                return response
            else:
                print("could be external")
                # check if the file has been uploaded externally
                form = self.upload_file_form(request.POST, request.FILES)
                print(request.FILES)
                # if yes - save file and create a new application with it
                print(form)
                if form.is_valid():
                    print("form valid")
                    document = form.save(commit=False)
                    document.uploader = request.user
                    original_name = request.FILES.get("file").name
                    document.name = original_name.rsplit('.', 1)[0]
                    document.save()

                    application = Application.objects.create(applicant = request.user, position = offer, supplied_cv = document)
                    application.save()

                    message = MessageContext(
                        type="success",
                        message="Applied successfully",
                        action=MessageAction()
                    )
                    context = {
                        "message": message.as_context(),
                    }
                    html = render_to_string(self.application_message, context = context, request = request)
                    response = HttpResponse(html)
                    response.headers["HX-Trigger"] = '{"closeModal":true}'
                    return response
                else:
                # if no - return message that file is needed
                    message = MessageContext(
                        type="error",
                        message="Form is invalid!",
                        action=MessageAction()
                    )
                    context = {
                        "message": message.as_context(),
                    }
                return render(request, self.application_message, context = context)



class ApplicationWithExternalFileModal(View):

    template = "jobs/components/application_file_external.html"
    form = DocumentForm

    def get(self,request):

        context = {
            "form": self.form(),
        }

        return render(request, self.template, context = context)
    

class ApplicationWithInternalFileModal(View):

    template = "jobs/components/application_file_internal.html"

    def get(self,request):
        from main.models import FileSourceTypeChoices
        # get  user document (CVs)
        user = request.user
        internal_docs = Document.objects.filter(uploader = user, source_type = FileSourceTypeChoices.INTERNAL)
        # convert the docs into absolute urls and servee theme instead
        docs = [
            {
                "id": doc.id,
                "name": doc.name,
                "url": doc.get_absolute_url(),
            }
            for doc in internal_docs
        ]
        # context = {
        #     "internal_docs": docs if len(docs) > 0 else [
        #         {
        #             "id": x,
        #             "name": str(x),
        #             "url": "http:/"+str(x),
        #         } for x in range(3)
        #     ],
        # }
        context = {
            "internal_docs": docs,
        }
        print(context)
        return render(request, self.template, context = context)



class BookamrkOfferView(View):

    def post(self, request, offer_id : int):

        offer = get_object_or_404(Offer, id=offer_id)
        user = get_object_or_404(User, email = request.user)
        if Bookmark.objects.filter(bookmarked_offer = offer, bookmarked_by = user).exists():
            #the offer is already bookmarked
            return HttpResponse(content = "The offer is already bookmarked")
        
        bookmark = Bookmark.objects.create(bookmarked_offer = offer, bookmarked_by = user)
        bookmark.save()
        return HttpResponse(content = "Bookmarked successfully")
    

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

