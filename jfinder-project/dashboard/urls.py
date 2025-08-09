from django.urls import path, include
from .views import *

urlpatterns = [
    path("", DashbaordBaseView.as_view(), name="dashboard"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("bookmarked/", BookmarkedListView.as_view(), name="bookmarked"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("trend-plot/", TrendPlotView.as_view(), name = "trend_plot"),
]
