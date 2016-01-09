from rest_framework import serializers
from lines import models


class DailyScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DailySchedule


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
