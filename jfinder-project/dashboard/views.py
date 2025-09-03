from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View, ListView

from copy import deepcopy

from authentication.forms import PasswordChangeForm, EmailChangeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
from plotly.io import to_html

def plot1():
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = to_html(Scatter(x=x_data, y=y_data,
                        mode='lines+markers', name='test',
                        opacity=0.8, marker_color='green',),
               full_html=False, include_plotlyjs="cdn")
    return {"plot": plot_div, "id": "plot_1"}

def plot2():
    random_x = [100, 2000, 550]
    names = ['A', 'B', 'C']
    fig = px.pie(values=random_x, names=names)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor="LightSteelBlue")
    plot_div2 = to_html(fig, include_plotlyjs="cdn")
    return {"plot": plot_div2, "id": "plot_2"}

# Create your views here.

NAV_ELEMENTS = {
    'profile': {
        "label": "Profile",
        "url": reverse_lazy("profile"),
        "selected": False,
        "section": "personal",
    },
    'bookmars': {
        "label": "Bookmarks",
        "url": reverse_lazy("bookmarks"),
        "selected": False,
        "section": "activity",
    },
    'inbox': {
        "label": "Inbox",
        "url": reverse_lazy("inbox"),
        "selected": False,
        "section": "activity",
    },
    'stats': {
        "label": "Stats",
        "url": reverse_lazy("stats"),
        "selected": False,
        "section": "activity",
    },
    'settings': {
        "label": "Settings",
        "url": reverse_lazy("settings"),
        "selected": False,
        "section": "personal",
    },
    'cvbuilder': {
        "label": "CV Builder",
        "url": reverse_lazy("cvbuilder"),
        "selected": False,
        "section": "personal",
    },
}

class DashbaordBaseView(View):

    def get(self, request, selected: str = "profile"):
        print("Selected:", selected)
        selected_default = 'profile'
        selected_nav_url = ""
        nav_elements = deepcopy(NAV_ELEMENTS)
        if selected in NAV_ELEMENTS.keys():
            nav_elements[selected]['selected'] = True
            selected_nav_url = nav_elements[selected]['url']
        else:
            nav_elements[selected_default]['selected'] = True
            selected_nav_url = nav_elements[selected_default]['url']
        context = {
            "navigation": nav_elements,
            "selected": selected_nav_url,
        }
        print(context)
        return render(request, 'dashboard/base.html', context=context)

    def post(self, request):
        return

@method_decorator(login_required, name="dispatch")
class SettingsView(View):

    def get(self, request):
        context = {
            'email_change_form' : EmailChangeForm(user=request.user),
            'password_change_form' : PasswordChangeForm(user=request.user),
        }
        return render(request, 'dashboard/components/settings.html', context=context)

    def post(self, request):
        return


@method_decorator(login_required, name="dispatch")
class InboxView(View):

    def get(self, request):
        return render(request, "dashboard/components/inbox.html", context={})

    def post(self, request):
        # most likely the logic here would be sending responses to the emails in the inbox
        return


@method_decorator(login_required, name="dispatch")
class StatsView(View):

    def get(self, request):
        return render(request, "dashboard/components/stats.html", context={})

    def post(self, request):
        return


@method_decorator(login_required, name="dispatch")
class BookmarkedListView(ListView):

    def get(self, request):
        return render(request, "dashboard/components/bookmarked.html", context={})

    def post(self, request):
        # adding to the bookmarked list from anywhere
        return
    

@method_decorator(login_required, name="dispatch")
class TrendPlotView(View):

    def get(self, request):
        #generate here 3 plots for week, month and year options
        #generate a context with html representations of every one of them
        #while generating give each a unique id
        #render a simple template with those 3 plots there
        #the htmx request will use hx-select to get only wht it needs
        context = {"plots": [
            plot2(),
            plot1(),
        ]}
        return render(request, 'dashboard/components/trend_plot.html', context = context)
    
