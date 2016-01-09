from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from lines.utils import times_gte


class Line(models.Model):
    name = models.CharField(max_length=200)


class Station(models.Model):
    name = models.CharField(max_length=200)
    line = models.ForeignKey(Line)

    def register_daily_times(self, days, times):
        for day in days:
            for time in times:
                DailySchedule.objects.create(station=self, day=day, time=time)

    def daily_times(self, day):
        return [s.time for s in DailySchedule.objects.filter(station=self, day=day)]

    def next_daily_times(self, day, t=None, count=3):
        if t is None:
            t = timezone.now().time()
        return times_gte(self.daily_times(day), t)[:count]

    def register_dates(self, dates):
        for date in dates:
            GeneralSchedule.objects.create(station=self, date=date)

    def dates(self):
        return [s.date for s in GeneralSchedule.objects.filter(station=self)]


class DailySchedule(models.Model):
    MONDAY = 'mon'
    TUESDAY = 'tue'
    SATURDAY = 'sat'
    SUNDAY = 'sun'
    WEEKDAYS = [MONDAY, TUESDAY]

    station = models.ForeignKey(Station)
    day = models.CharField(max_length=30)
    time = models.TimeField()


class GeneralSchedule(models.Model):
    station = models.ForeignKey(Station)
    date = models.DateTimeField()


class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    stations = models.ManyToManyField(Station)

    def next_daily_times(self, day, t=None, count=3):
        result = []
        for station in self.stations.all():
            for t2 in station.next_daily_times(day, t, count):
                result.append((station.line, t2))

        result = sorted(result, key=lambda x: x[1])
        return result[:count]
