from django.urls import path

from .views import *

urlpatterns = [
    
    # DASHBOARD Views...
    path("analysis/", EntityModelListView.as_view()),
    path('<slug:entity_slug>/analysis/dashboard/',
         EntityModelDetailView.as_view(),
         name='entity-dashboard-analysis'),
    path('<slug:entity_slug>/analysis/dashboard/year/<int:year>/',
         FiscalYearEntityModelDashboardView.as_view(),
         name='entity-dashboard-year'),
    path('<slug:entity_slug>/analysis/dashboard/quarter/<int:year>/<int:quarter>/',
         QuarterlyEntityDashboardView.as_view(),
         name='entity-dashboard-quarter'),
    path('<slug:entity_slug>/analysis/dashboard/month/<int:year>/<int:month>/',
         MonthlyEntityDashboardView.as_view(),
         name='entity-dashboard-month'),
    path('<slug:entity_slug>/analysis/dashboard/date/<int:year>/<int:month>/<int:day>/',
         DateEntityDashboardView.as_view(),
         name='entity-dashboard-date'),

]
