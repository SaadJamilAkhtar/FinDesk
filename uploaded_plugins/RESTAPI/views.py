from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_ledger.models.entity import EntityModel
from django_ledger.views import LoginRequiredMixIn
from .serializers import EntitySerializer
from django.utils.translation import gettext as _


class EntityView(APIView):
    def get(self, request, format=None):
        snippets = EntityModel.objects.all()
        serializer = EntitySerializer(snippets, many=True)
        return Response(serializer.data)


class main(LoginRequiredMixIn, ListView):
    template_name = 'RESTAPI/main.html'
    PAGE_TITLE = _('DOCS')
    context_object_name = 'entities'
    extra_context = {
        'page_title': PAGE_TITLE,
        'header_title': PAGE_TITLE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_subtitle'] = self.request.user.get_full_name()
        context['header_subtitle_icon'] = 'ei:user'
        return context

    def get_queryset(self):
        return EntityModel.objects.for_user(
            user_model=self.request.user
        )
