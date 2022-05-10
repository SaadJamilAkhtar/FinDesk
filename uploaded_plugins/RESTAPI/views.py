from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django_ledger.models.entity import EntityModel
from .serializers import EntitySerializer


class EntityView(APIView):
    def get(self, request, format=None):
        snippets = EntityModel.objects.all()
        serializer = EntitySerializer(snippets, many=True)
        return Response(serializer.data)
