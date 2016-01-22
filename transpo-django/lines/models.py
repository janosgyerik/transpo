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

    def find_daily_times(self, query, day):
        # check for holiday
        # TODO

        # check for specific day
        specific_day_query = query.filter(day=day)
        if specific_day_query.exists():
            return specific_day_query

        # check for weekday or weekend
        weekday_weekend_label = DailySchedule.weekday_weekend_label(day)
        weekday_weekend_query = query.filter(day=weekday_weekend_label)
        if weekday_weekend_query.exists():
            return weekday_weekend_query

        # check for daily
        daily_query = query.filter(day=DailySchedule.DAILY)
        if daily_query.exists():
            return daily_query

        return query

    def next_daily_times(self, date=None):
        query = self.dailyschedule_set.all()
        if date is not None:
            day = '{:%a}'.format(date)
            query = self.find_daily_times(query, day)

            # note: strange that this doesn't work:
            # timestr = '{:%H:%M}'.format(date.time)
            timestr = date.strftime('%H:%M')

            return query.filter(time__gte=timestr)

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
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thu'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'

    _WEEKDAYS = {MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY}
    _WEEKENDS = {SATURDAY, SUNDAY}

    WEEKDAYS = 'weekdays'
    WEEKENDS = 'weekends'
    DAILY = 'daily'

    station = models.ForeignKey(Station)
    day = models.CharField(max_length=30)
    time = models.TimeField()

    def __str__(self):
        return '{}/{}/{}'.format(self.station, self.day, self.time)

    @property
    def day_and_time(self):
        return '({}) {:%H:%M}'.format(self.day, self.time)

    @staticmethod
    def weekday_weekend_label(day):
        if day in DailySchedule._WEEKDAYS:
            return DailySchedule.WEEKDAYS
        elif day in DailySchedule._WEEKENDS:
            return DailySchedule.WEEKENDS
        return 'ERROR'


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

    def __str__(self):
        return '{} ({})'.format(self.name, ', '.join([str(x) for x in self.stations.all()]))
