from django.db import models
from lines.utils import times_gte


class Line(models.Model):
    name = models.CharField(max_length=200)


class Station(models.Model):
    line = models.ForeignKey(Line)
    name = models.CharField(max_length=200)

    def register_daily_times(self, days, times):
        for day in days:
            for time in times:
                DailySchedule.objects.create(station=self, day=day, time=time)

    def daily_times(self, day):
        return [s.time for s in DailySchedule.objects.filter(station=self, day=day)]

    def next_daily_times(self, day, t, count=3):
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
