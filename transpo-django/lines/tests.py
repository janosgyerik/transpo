from django.test import TestCase
from django.utils.datetime_safe import time, datetime
from django.utils.timezone import get_current_timezone
from lines.models import Line, Station, DailySchedule
from lines.utils import times_gte


class DailyTimesTestCase(TestCase):
    line_name = 'R5'
    station_name = 'Jaures'
    weekday_times = [time(17, 6), time(17, 26), time(17, 46),
                     time(18, 6), time(18, 26), time(18, 46)]
    saturday_times = [time(17, 6)]

    def times(self, day):
        return self.station.daily_times(day)

    def setUp(self):
        line = Line.objects.create(name=self.line_name)
        self.station = station = Station.objects.create(line=line, name=self.station_name)
        station.register_daily_times(days=DailySchedule.WEEKDAYS, times=self.weekday_times)
        station.register_daily_times(days=[DailySchedule.SATURDAY], times=self.saturday_times)

        dummy_line = Line.objects.create(name='dummy line')
        dummy_station = Station.objects.create(line=dummy_line, name='dummy station')
        dummy_station.register_daily_times(days=[DailySchedule.MONDAY], times=self.weekday_times)
        dummy_station.register_daily_times(days=[DailySchedule.SUNDAY], times=self.saturday_times)

    def test_times_on_monday(self):
        self.assertEquals(self.weekday_times, self.times(DailySchedule.MONDAY))

    def test_times_on_tuesday(self):
        self.assertEquals(self.times(DailySchedule.MONDAY), self.times(DailySchedule.TUESDAY))

    def test_times_on_saturday(self):
        self.assertEquals(self.saturday_times, self.times(DailySchedule.SATURDAY))

    def test_times_on_sunday(self):
        self.assertEquals([], self.times(DailySchedule.SUNDAY))

    def test_next_times_when_empty(self):
        self.assertEquals([], self.station.next_daily_times(DailySchedule.SUNDAY, time(0, 0)))

    def test_next_times_before_first(self):
        day = DailySchedule.MONDAY
        before_first = time(0, 0)
        count = 3
        self.assertEquals(self.weekday_times[:count], self.station.next_daily_times(day, before_first, count))
        count = 4
        self.assertEquals(self.weekday_times[:count], self.station.next_daily_times(day, before_first, count))
        self.assertTrue(count < len(self.weekday_times))

    def test_next_times_after_first(self):
        day = DailySchedule.MONDAY
        after_first = self.weekday_times[1]
        times = self.weekday_times[1:]
        count = 3
        self.assertEquals(times[:count], self.station.next_daily_times(day, after_first, count))
        count = 4
        self.assertEquals(times[:count], self.station.next_daily_times(day, after_first, count))
        self.assertTrue(count < len(times))

    def test_next_times_at_last(self):
        day = DailySchedule.MONDAY
        at_last = self.weekday_times[-1]
        times = self.weekday_times[-1:]
        count = 3
        self.assertEquals(times[:count], self.station.next_daily_times(day, at_last, count))
        count = 4
        self.assertEquals(times[:count], self.station.next_daily_times(day, at_last, count))
        self.assertEquals(1, len(self.station.next_daily_times(day, at_last, count)))

    def test_time_gte_all_for_min(self):
        times = [time(0, 0), time(5, 5), time(7, 7)]
        self.assertEquals(times, times_gte(times, time.min))

    def test_time_gte_all_for_first(self):
        times = [time(0, 0), time(5, 5), time(7, 7)]
        self.assertEquals(times, times_gte(times, time.min))

    def test_time_gte_some(self):
        times = [time(0, 0), time(5, 5), time(7, 7)]
        self.assertEquals(times[1:], times_gte(times, times[1]))

    def test_time_gte_last_for_last(self):
        times = [time(0, 0), time(5, 5), time(7, 7)]
        self.assertEquals(times[-1:], times_gte(times, times[-1]))

    def test_time_gte_none_for_max(self):
        times = [time(0, 0), time(5, 5), time(7, 7)]
        self.assertEquals([], times_gte(times, time.max))


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
