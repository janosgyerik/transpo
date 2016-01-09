from django.test import TestCase
from django.utils.datetime_safe import time, datetime
from django.utils.timezone import get_current_timezone
from lines.models import Line, Station, DailySchedule


class DailyTimesTestCase(TestCase):
    line_name = 'R5'
    station_name = 'Jaures'
    weekday_times = [time(17, 6), time(17, 26), time(17, 46)]
    saturday_times = [time(17, 6)]

    def times(self, day):
        return self.station.daily_times(day)

    def setUp(self):
        line = Line.objects.create(name=self.line_name)
        self.station = station = Station.objects.create(line=line, name=self.station_name)
        station.register_daily_times(days=DailySchedule.WEEKDAYS, times=self.weekday_times)
        station.register_daily_times(days=[DailySchedule.SATURDAY], times=self.saturday_times)

    def test_times_on_monday(self):
        self.assertEquals(self.weekday_times, self.times(DailySchedule.MONDAY))

    def test_times_on_tuesday(self):
        self.assertEquals(self.times(DailySchedule.MONDAY), self.times(DailySchedule.TUESDAY))

    def test_times_on_saturday(self):
        self.assertEquals(self.saturday_times, self.times(DailySchedule.SATURDAY))

    def test_times_on_sunday(self):
        self.assertEquals([], self.times(DailySchedule.SUNDAY))


class GeneralScheduleTestCase(TestCase):
    def test_nonempty_dates(self):
        dates = [datetime(2016, 1, 19, 9, 41, tzinfo=get_current_timezone())]
        line = Line.objects.create(name='TGV 6911')
        station = Station.objects.create(line=line, name='Paris-Gare-de-Lyon')
        station.register_dates(dates=dates)
        self.assertEquals(dates, station.dates())

    def test_empty_dates(self):
        dates = []
        line = Line.objects.create(name='TGV 6911')
        station = Station.objects.create(line=line, name='Paris-Gare-de-Lyon')
        station.register_dates(dates=dates)
        self.assertEquals(dates, station.dates())
