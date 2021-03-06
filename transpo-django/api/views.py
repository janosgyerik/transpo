from django import forms
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from lines import models
from api import serializers
from rest_framework.response import Response


class StationViewSet(viewsets.ModelViewSet):
    queryset = models.Station.objects.all()
    serializer_class = serializers.StationSerializer


class StationTimesForm(forms.Form):
    date = forms.DateTimeField(required=False)
    time = forms.TimeField(required=False)

    def parse_date(self):
        if self.cleaned_data['date'] is not None:
            date = self.cleaned_data['date']
        elif 'date' in self.data:
            date = timezone.now()
        else:
            date = None

        if self.cleaned_data['time'] is not None:
            t = self.cleaned_data['time']
            if date is None:
                date = timezone.now()
            date = date.replace(hour=t.hour, minute=t.minute)
        return date


class StationTimesViewSet(viewsets.ModelViewSet):
    queryset = models.DailySchedule.objects.all()
    serializer_class = serializers.DailyScheduleSerializer

    def list(self, request, station_id):
        form = StationTimesForm(request.GET)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        station = get_object_or_404(models.Station, pk=station_id)
        date = form.parse_date()
        times = station.next_daily_times(date)

        page = self.paginate_queryset(times)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(times, many=True)
        return Response(serializer.data)


class LineViewSet(viewsets.ModelViewSet):
    queryset = models.Line.objects.all()
    serializer_class = serializers.LineSerializer


class DailyScheduleViewSet(viewsets.ModelViewSet):
    queryset = models.DailySchedule.objects.all()
    serializer_class = serializers.DailyScheduleSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer


class LocationTimesViewSet(viewsets.ModelViewSet):
    queryset = models.DailySchedule.objects.all()
    serializer_class = serializers.DailyScheduleSerializer

    def list(self, request, location_id):
        form = StationTimesForm(request.GET)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        location = get_object_or_404(models.Location, pk=location_id)
        date = form.parse_date()
        times = location.next_daily_times(date)

        page = self.paginate_queryset(times)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(times, many=True)
        return Response(serializer.data)
