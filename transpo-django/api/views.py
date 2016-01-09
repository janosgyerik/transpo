from rest_framework import viewsets
from lines import models
from api import serializers
from rest_framework.response import Response


class StationListViewSet(viewsets.ModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer


class StationTimesViewSet(viewsets.ModelViewSet):
    queryset = models.DailySchedule.objects.all()
    serializer_class = serializers.DailyScheduleSerializer

    def list(self, request, station_id):
        times = models.DailySchedule.objects.filter(station_id=station_id)
        page = self.paginate_queryset(times)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(times, many=True)
        return Response(serializer.data)
