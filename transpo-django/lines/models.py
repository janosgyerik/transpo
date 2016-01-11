from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Line(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Station(models.Model):
    name = models.CharField(max_length=200)
    line = models.ForeignKey(Line)

    def register_daily_times(self, days, times):
        for day in days:
            for time in times:
                DailySchedule.objects.create(station=self, day=day, time=time)

    def daily_times(self, date=None):
        if date is None:
            date = timezone.now()
        date = date.replace(hour=0, minute=0, second=0)
        return self.next_daily_times(date)

    def next_daily_times(self, date=None):
        query = self.dailyschedule_set.all()
        if date is not None:
            day = '{:%a}'.format(date)
            # note: strange that this doesn't work:
            # timestr = '{:%H:%M}'.format(date.time)
            timestr = date.strftime('%H:%M')
            query = query.filter(day=day, time__gte=timestr)
        return query

    def register_dates(self, dates):
        for date in dates:
            GeneralSchedule.objects.create(station=self, date=date)

    def dates(self):
        return [s.date for s in GeneralSchedule.objects.filter(station=self)]

    def __str__(self):
        return '{}/{}'.format(self.line, self.name)


class DailySchedule(models.Model):
    MONDAY = 'Mon'
    TUESDAY = 'Tue'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'
    WEEKDAYS = [MONDAY, TUESDAY]

    station = models.ForeignKey(Station)
    day = models.CharField(max_length=30)
    time = models.TimeField()

    def __str__(self):
        return '{}/{}/{}'.format(self.station, self.day, self.time)


class GeneralSchedule(models.Model):
    station = models.ForeignKey(Station)
    date = models.DateTimeField()


class Location(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    stations = models.ManyToManyField(Station)

    def next_daily_times(self, date=None):
        result = []
        for station in self.stations.all():
            result += list(station.next_daily_times(date))

        return sorted(result, key=lambda x: x.time)
