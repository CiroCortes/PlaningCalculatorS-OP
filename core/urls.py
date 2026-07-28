from django.urls import path
from .views import SOPDashboardView

urlpatterns = [
    path('', SOPDashboardView.as_view(), name='sop_dashboard'),
]
