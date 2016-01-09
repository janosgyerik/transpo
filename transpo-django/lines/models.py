from django.db import models


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


class DailySchedule(models.Model):
    MONDAY = 'mon'
    TUESDAY = 'tue'
    SATURDAY = 'sat'
    SUNDAY = 'sun'
    WEEKDAYS = [MONDAY, TUESDAY]

    station = models.ForeignKey(Station)
    day = models.CharField(max_length=30)
    time = models.TimeField()
