from rest_framework import serializers
from .models import ActivityDetails


class ActivityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityDetails
        fields = '__all__'

