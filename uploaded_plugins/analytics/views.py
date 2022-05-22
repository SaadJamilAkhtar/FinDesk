

from datetime import timedelta
from random import randint

from django.contrib.messages import add_message, ERROR
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import localtime, localdate
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView,RedirectView


from django_ledger.models import (EntityModel)

from django_ledger.views.mixins import (
    QuarterlyReportMixIn, YearlyReportMixIn,
    MonthlyReportMixIn, DateReportMixIn, LoginRequiredMixIn, SessionConfigurationMixIn, EntityUnitMixIn,
    EntityDigestMixIn, UnpaidElementsMixIn, BaseDateNavigationUrlMixIn
)



class EntityModelListView(LoginRequiredMixIn, ListView):
    template_name = 'analytics/entity_list_analytics.html'
    context_object_name = 'entities'
    PAGE_TITLE = _('My Entities')
    extra_context = {
        'header_title': PAGE_TITLE,
        'page_title': PAGE_TITLE
    }

    def get_queryset(self):
        return EntityModel.objects.for_user(
            user_model=self.request.user)


# DASHBOARD VIEWS 
class EntityModelDetailView(LoginRequiredMixIn,
                            EntityUnitMixIn,
                            RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        loc_date = localdate()
        unit_slug = self.get_unit_slug()
        if unit_slug:
            return reverse('unit-dashboard-month',
                           kwargs={
                               'entity_slug': self.kwargs['entity_slug'],
                               'unit_slug': unit_slug,
                               'year': loc_date.year,
                               'month': loc_date.month,
                           })
        return reverse('analytics:entity-dashboard-month',
                       kwargs={
                           'entity_slug': self.kwargs['entity_slug'],
                           'year': loc_date.year,
                           'month': loc_date.month,
                       })


class FiscalYearEntityModelDashboardView(LoginRequiredMixIn,
                                         SessionConfigurationMixIn,
                                         BaseDateNavigationUrlMixIn,
                                         UnpaidElementsMixIn,
                                         EntityUnitMixIn,
                                         EntityDigestMixIn,
                                         YearlyReportMixIn,
                                         DetailView):
    context_object_name = 'entity'
    slug_url_kwarg = 'entity_slug'
    template_name = 'analytics/entity_dashboard_analytics.html'
    DJL_NO_FROM_DATE_RAISE_404 = False
    DJL_NO_TO_DATE_RAISE_404 = False

    FETCH_UNPAID_BILLS = True
    FETCH_UNPAID_INVOICES = True

    def get_context_data(self, **kwargs):
        context = super(FiscalYearEntityModelDashboardView, self).get_context_data(**kwargs)
        entity_model: EntityModel = self.object
        context['page_title'] = entity_model.name
        context['header_title'] = entity_model.name
        context['header_subtitle'] = _('Dashboard')
        context['header_subtitle_icon'] = 'mdi:monitor-dashboard'

        unit_slug = context.get('unit_slug', self.get_unit_slug())
        KWARGS = dict(entity_slug=self.kwargs['entity_slug'])

        if unit_slug:
            KWARGS['unit_slug'] = unit_slug

        url_pointer = 'entity' if not unit_slug else 'unit'
        context['pnl_chart_id'] = f'djl-entity-pnl-chart-{randint(10000, 99999)}'
        context['pnl_chart_endpoint'] = reverse(f'django_ledger:{url_pointer}-json-pnl',
                                                kwargs=KWARGS)
        context['payables_chart_id'] = f'djl-entity-payables-chart-{randint(10000, 99999)}'
        context['payables_chart_endpoint'] = reverse(f'django_ledger:{url_pointer}-json-net-payables',
                                                     kwargs=KWARGS)
        context['receivables_chart_id'] = f'djl-entity-receivables-chart-{randint(10000, 99999)}'
        context['receivables_chart_endpoint'] = reverse(f'django_ledger:{url_pointer}-json-net-receivables',
                                                        kwargs=KWARGS)

        context = self.get_entity_digest(context)

        return context

    def get_fy_start_month(self) -> int:
        entity_model: EntityModel = self.object
        return entity_model.fy_start_month

    def get_queryset(self):
        """
        Returns a queryset of all Entities owned or Managed by the User.
        Queryset is annotated with user_role parameter (owned/managed).
        :return: The View queryset.
        """
        return EntityModel.objects.for_user(
            user_model=self.request.user).select_related('coa')


class QuarterlyEntityDashboardView(FiscalYearEntityModelDashboardView, QuarterlyReportMixIn):
    """
    Entity Quarterly Dashboard View.
    """


class MonthlyEntityDashboardView(FiscalYearEntityModelDashboardView, MonthlyReportMixIn):
    """
    Monthly Entity Dashboard View.
    """


class DateEntityDashboardView(FiscalYearEntityModelDashboardView, DateReportMixIn):
    """
    Date-specific Entity Dashboard View.
    """

