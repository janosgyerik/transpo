from django.test import TestCase
from django.utils.datetime_safe import time
from lines.models import Line, Station, Schedule


class TimeTableTestCase(TestCase):
    line_name = 'R5'
    station_name = 'Jaures'
    weekday_times = [time(17, 6), time(17, 26), time(17, 46)]
    saturday_times = [time(17, 6)]

    def times(self, day):
        return self.station.times(day)

    def setUp(self):
        line = Line.objects.create(name=self.line_name)
        self.station = station = Station.objects.create(line=line, name=self.station_name)
        station.register_times(days=Schedule.WEEKDAYS, times=self.weekday_times)
        station.register_times(days=[Schedule.SATURDAY], times=self.saturday_times)

    def test_times_on_monday(self):
        self.assertEquals(self.weekday_times, self.times(Schedule.MONDAY))

    def test_times_on_tuesday(self):
        self.assertEquals(self.times(Schedule.MONDAY), self.times(Schedule.TUESDAY))

    def test_times_on_saturday(self):
        self.assertEquals(self.saturday_times, self.times(Schedule.SATURDAY))

    def test_times_on_sunday(self):
        self.assertEquals([], self.times(Schedule.SUNDAY))
