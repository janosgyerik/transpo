from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import time, datetime
from django.utils.timezone import get_current_timezone
from lines.models import Line, Station, DailySchedule, Location
from lines.utils import times_gte


def dayname(date):
    return date.strftime('%a')


class DailyTimesTestCase(TestCase):
    weekday_date = datetime(2016, 1, 11)
    weekday_datestr = weekday_date.strftime('%Y-%m-%d')

    weekend_date = datetime(2016, 1, 10)
    weekend_datestr = weekend_date.strftime('%Y-%m-%d')

    line_name = 'R5'
    station_name = 'Jaures'

    weekday_times = [time(17, 6), time(17, 26), time(17, 46), time(18, 6)]
    weekend_times = [time(9, 34), time(10, 34), time(11, 34)]
    saturday_times = [time(17, 6)]

    def _times(self, times):
        return [s.time for s in times]

    def next_weekday(self, weekday):
        d = timezone.now()
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + timedelta(days_ahead)

    def setUp(self):
        line = Line.objects.create(name=self.line_name)
        self.station = station = Station.objects.create(line=line, name=self.station_name)
        station.register_daily_times(days=[DailySchedule.WEEKDAYS], times=self.weekday_times)
        station.register_daily_times(days=[DailySchedule.WEEKENDS], times=self.weekend_times)
        station.register_daily_times(days=[DailySchedule.SATURDAY], times=self.saturday_times)

    def test_mon_finds_weekdays(self):
        self.assertEquals(self.weekday_times, self._times(self.station.daily_times(self.next_weekday(0))))

    def test_tue_finds_weekdays(self):
        self.assertEquals(self.weekday_times, self._times(self.station.daily_times(self.next_weekday(1))))

    def test_sat_finds_sat(self):
        self.assertEquals(self.saturday_times, self._times(self.station.daily_times(self.next_weekday(5))))

    def test_sun_finds_weekends(self):
        self.assertEquals(self.weekend_times, self._times(self.station.daily_times(self.next_weekday(6))))

    def test_times_on_tuesday(self):
        self.assertEquals(
            self._times(self.station.daily_times(self.next_weekday(0))),
            self._times(self.station.daily_times(self.next_weekday(1)))
        )

    def test_times_on_saturday(self):
        self.assertEquals(self.saturday_times, self._times(self.station.daily_times(self.next_weekday(5))))

    def test_next_times_before_first(self):
        self.assertEquals(self.weekday_times, self._times(self.station.next_daily_times(self.weekday_date)))

    def test_next_times_after_first(self):
        after_first = self.weekday_times[1]
        monday = self.next_weekday(0).replace(hour=after_first.hour, minute=after_first.minute)
        times = self.weekday_times[1:]
        self.assertEquals(times, self._times(self.station.next_daily_times(monday)))

    def test_next_times_at_last(self):
        at_last = self.weekday_times[-1]
        monday = self.next_weekday(0).replace(hour=at_last.hour, minute=at_last.minute)
        times = self.weekday_times[-1:]
        self.assertEquals(times, self._times(self.station.next_daily_times(monday)))

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


class LocationTestCase(TestCase):
    def setUp(self):
        station_name = 'Saint-Germain-en-Laye'

        self.line1 = Line.objects.create(name='R1')
        self.station1 = Station.objects.create(name=station_name, line=self.line1)

        self.line2 = Line.objects.create(name='R5')
        self.station2 = Station.objects.create(name=station_name, line=self.line2)

        user = User.objects.create()
        self.location = Location.objects.create(user=user, name='Work')
        self.location.stations.add(self.station1, self.station2)

    def _linetimes(self, dailyschedules):
        return [(s.station.line, s.time) for s in dailyschedules]

    def test_combined_times_all_from_line1(self):
        date = timezone.now().date()
        day = dayname(date)

        other_date = date + timedelta(days=1)
        other_day = dayname(other_date)

        self.station1.register_daily_times([day], [time(17, 1), time(17, 11), time(17, 21), time(17, 31)])
        self.station2.register_daily_times([other_day], [time(17, 6), time(17, 26), time(17, 46), time(18, 6)])

        times = self._linetimes(self.location.next_daily_times(date))

        expected = [
            (self.line1, time(17, 1)),
            (self.line1, time(17, 11)),
            (self.line1, time(17, 21)),
            (self.line1, time(17, 31)),
        ]
        self.assertEquals(expected, times)

    def test_combined_times_all_from_line2(self):
        date = timezone.now().replace(hour=17, minute=1)
        day = dayname(date)

        self.station1.register_daily_times([day], [time(11, 1), time(11, 11), time(11, 21), time(11, 31)])
        self.station2.register_daily_times([day], [time(17, 6), time(17, 26), time(17, 46), time(18, 6)])

        times = self._linetimes(self.location.next_daily_times(date))

        expected = [
            (self.line2, time(17, 6)),
            (self.line2, time(17, 26)),
            (self.line2, time(17, 46)),
            (self.line2, time(18, 6)),
        ]
        self.assertEquals(expected, times)

    def test_combined_times_mix_from_both_line1_first(self):
        date = timezone.now().replace(hour=17, minute=20)
        day = dayname(date)

        self.station1.register_daily_times([day], [time(17, 1), time(17, 11), time(17, 21), time(17, 31)])
        self.station2.register_daily_times([day], [time(17, 6), time(17, 26), time(17, 46), time(18, 6)])

        times = self._linetimes(self.location.next_daily_times(date))

        expected = [
            (self.line1, time(17, 21)),
            (self.line2, time(17, 26)),
            (self.line1, time(17, 31)),
            (self.line2, time(17, 46)),
            (self.line2, time(18, 6)),
        ]
        self.assertEquals(expected, times)
