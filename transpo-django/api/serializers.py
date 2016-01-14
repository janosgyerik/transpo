from rest_framework import serializers
from lines import models


class DailyScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.DailySchedule


class StationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Station


class LineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Line


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Location
