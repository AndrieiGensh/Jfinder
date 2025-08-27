from django.urls import path, include
from dashboard.views import *

urlpatterns = [
    path("<str:selected>", DashbaordBaseView.as_view(), name="dashboard"),
    path("", DashbaordBaseView.as_view(), name="dashboard"),
    path("navigation/stats/", StatsView.as_view(), name="stats"),
    path("navigation/inbox/", InboxView.as_view(), name="inbox"),
    path("navigation/bookmarkes/", BookmarkedListView.as_view(), name="bookmarks"),
    path("navigation/settings/", SettingsView.as_view(), name="settings"),
    path("navigation/trend-plot/", TrendPlotView.as_view(), name = "trend_plot"),
]