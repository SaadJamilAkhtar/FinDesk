from rest_framework import serializers
from django_ledger.models.entity import EntityModel


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityModel
        fields = '__all__'
