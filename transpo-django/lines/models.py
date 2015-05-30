from django.db import models


class Line(models.Model):
    name = models.CharField(max_length=200)


class Station(models.Model):
    name = models.CharField(max_length=200)


class LineStation(models.Model):
    line = models.ForeignKey(Line)
    station = models.ForeignKey(Station)


class DailyScheduleDescriptor(models.Model):
    # comma separated value of short weekday names
    # example: sat, sun
    # example: mon, wed, thu, fri
    days = models.CharField(max_length=100)


class LineStationDailySchedule(models.Model):
    line = models.ForeignKey(Line)
    station = models.ForeignKey(Station)

    # exceptional days should come first to be matched first
    priority = models.IntegerField()

    descriptor = models.ForeignKey(DailyScheduleDescriptor)


class DailyScheduleTime(models.Model):
    schedule = models.ForeignKey(LineStationDailySchedule)
    hour = models.IntegerField()
    minute = models.IntegerField()


class LineStationGenericSchedule(models.Model):
    line = models.ForeignKey(Line)
    station = models.ForeignKey(Station)
    date = models.DateTimeField()
