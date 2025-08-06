from django.urls import path, include
from .views import *

urlpatterns = [
    path("", DashbaordBaseView.as_view(), name="dashboard"),
    path("stats/", StatsView.as_view(), name="stats"),
    path("inbox/", InboxView.as_view(), name="inbox"),
    path("bookmarked/", BookmarkedListView.as_view(), name="bookmarked"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("settings/delete-account-modal/", SettingsAccountDeleteModalView.as_view(), name="settings_delete_account_modal"),
    path('settings/change-account-info/', SettingsChangeAccountInfoView.as_view(), name="settings_change_account_info"),
    path('settings/change_password/', SettingsChangePasswordView.as_view(), name="settings_change_password"),
    path("trend-plot/", TrendPlotView.as_view(), name = "trend_plot"),
]
