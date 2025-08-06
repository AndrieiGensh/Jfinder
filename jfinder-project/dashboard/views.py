from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView
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

class DashbaordBaseView(View):

    def get(self, request):
        context = {
            "navigation": [
                {
                    'url': '/dashboard/inbox',
                    'label': 'Inbox',
                    'is_selected': False,
                },
                {
                    'url': '/dashboard/stats',
                    'label': 'Stats',
                    'is_selected': True,
                },
                {
                    'url': '/dashboard/bookmarked',
                    'label': 'Bookmarked',
                    'is_selected': False,
                },
                {
                    'url': '/dashboard/settings',
                    'label': 'Settings',
                    'is_selected': False,
                },
                {
                    'url': '/cvbuilder/',
                    'label': 'CVBuilder',
                    'is_selected': False,
                },
            ]
        }
        return render(request, 'dashboard/base.html', context=context)

    def post(self, request):
        return


class SettingsView(View):

    def get(self, request):
        return render(request, 'dashboard/components/settings.html', context={})

    def post(self, request):
        return
    

class SettingsAccountDeleteModalView(View):

    template_name = 'dashboard/components/delete_account_modal.html'
    template_ok_response = 'dashboard/components/delete_account_modal_response_ok.html'
    template_error_response = 'dashboard/components/delete_account_modal_response_error.html'

    def get(self, request):
        return render(request, self.template_name, context = {})
    
    def post(self, request):
        password = request.POST['delete-account-password']
        context = {}
        print(password)
        if password == "test_ok":
            context['message'] = "Deletion confirmed. See ypu later!"
            return render(request, self.template_ok_response, context=context)
        context['message'] = "Wrong password provided"
        return render(request, self.template_error_response, context=context)
    

class SettingsChangeAccountInfoView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class SettingsChangePasswordView(View):

    def get(self, request):
        pass

    def post(self, request):
        current_password = request.POST["current-password"]
        new_password = request.POST["new-password"]
        new_password_repeat = request.POST["new-password-confirm"]
        # DO THIS WITH DJANGO FORMS!!!






class InboxView(View):

    def get(self, request):
        return render(request, "dashboard/components/inbox.html", context={})

    def post(self, request):
        # most likely the logic here would be sending responses to the emails in the inbox
        return


class StatsView(View):

    def get(self, request):
        return render(request, "dashboard/components/stats.html", context={})

    def post(self, request):
        return


class BookmarkedListView(ListView):

    def get(self, request):
        return render(request, "dashboard/components/bookmarked.html", context={})

    def post(self, request):
        # adding to the bookmarked list from anywhere
        return
    

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
    
