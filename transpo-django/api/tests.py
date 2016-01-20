import json
from datetime import timedelta
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.datetime_safe import time
from django.utils import timezone
from django.utils.timezone import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from lines import models
from api import views

TESTSERVER_URL = 'http://testserver'


class StationTestCase(APITestCase):
    def test_no_stations(self):
        url = reverse('station-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], json.loads(response.content.decode()))

    def test_one_station(self):
        line = models.Line.objects.create(name='R5')
        station = models.Station.objects.create(name='Saint-Germain-en-Laye', line=line)

        url = reverse('station-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = json.loads(response.content.decode())
        self.assertEquals(1, len(results))

        expected = [
            {
                'url': TESTSERVER_URL + reverse('station-detail', kwargs={'pk': station.id}),
                'name': station.name,
                'line': TESTSERVER_URL + reverse('line-detail', kwargs={'pk': line.id}),
            }
        ]
        self.assertEquals(expected, results)


def to_json(response):
    return json.loads(response.content.decode())


def to_times(json_times):
    def to_time(s):
        parts = s.split(':')
        return time(int(parts[0]), int(parts[1]))
    return [to_time(s['time']) for s in json_times]


class StationTimesTestCase(TestCase):
    times = [time(17, 6), time(17, 26), time(17, 46), time(18, 6), time(18, 26)]

    service_date = datetime(2016, 1, 11)
    service_date_6pm = datetime(2016, 1, 11, 18)
    service_datestr = service_date.strftime('%Y-%m-%d')
    service_day = models.DailySchedule.MONDAY

    nonservice_date = datetime(2016, 1, 10)
    nonservice_datestr = nonservice_date.strftime('%Y-%m-%d')
    nonservice_day = models.DailySchedule.SUNDAY

    def baseurl(self, station_id=None):
        if station_id is None:
            station_id = self.station.id
        return reverse('station-times-list', kwargs={'station_id': station_id})

    def setUp(self):
        self.line = line = models.Line.objects.create(name='R5')
        self.station = station = models.Station.objects.create(name='Saint-Germain-en-Laye', line=line)
        station.register_daily_times([self.service_day], self.times)

    def test_nonexistent_station_gives_404(self):
        url = self.baseurl(self.station.id + 1)
        response = self.client.get(url)
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEquals({'detail': 'Not found.'}, to_json(response))

    def test_all_times(self):
        url = self.baseurl()
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = to_json(response)
        self.assertEquals(len(self.times), len(results))

    def test_invalid_date_param(self):
        url = self.baseurl() + '?date=malformed'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected = {
            'date': ['Enter a valid date/time.']
        }
        self.assertEquals(expected, to_json(response))

    def test_invalid_time_param(self):
        url = self.baseurl() + '?time=malformed'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected = {
            'time': ['Enter a valid time.']
        }
        self.assertEquals(expected, to_json(response))

    def test_all_times_on_service_day_by_date(self):
        url = self.baseurl() + '?date=' + self.service_datestr
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.times, to_times(to_json(response)))

    def test_no_times_on_nonservice_day_by_date(self):
        url = self.baseurl() + '?date=' + self.nonservice_datestr
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], to_json(response))

    def test_all_times_on_service_day_by_time(self):
        everyday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.station.register_daily_times(everyday, self.times)
        url = self.baseurl() + '?time=00:00'

        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.times, to_times(to_json(response)))

    def test_no_times_on_nonservice_day_by_time(self):
        self.station.dailyschedule_set.all().delete()
        url = self.baseurl() + '?time=00:00'

        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], to_times(to_json(response)))

    def test_times_after_6pm_by_date(self):
        url = self.baseurl() + '?date=' + self.service_datestr + ' 18:00'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.times[3:], to_times(to_json(response)))

    def test_times_after_6pm_by_time(self):
        everyday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.station.register_daily_times(everyday, self.times)
        url = self.baseurl() + '?time=18:00'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.times[3:], to_times(to_json(response)))


class LocationTimesTestCase(TestCase):
    line1_times = [time(17, 1), time(17, 11), time(17, 21), time(17, 31)]
    line2_times = [time(17, 6), time(17, 26), time(17, 46), time(18, 6)]

    service_date = datetime(2016, 1, 11)
    service_datestr = service_date.strftime('%Y-%m-%d')
    service_day = models.DailySchedule.MONDAY

    nonservice_date = datetime(2016, 1, 12)
    nonservice_datestr = nonservice_date.strftime('%Y-%m-%d')

    def baseurl(self, location_id=None):
        if location_id is None:
            location_id = self.location.id
        return reverse('location-times-list', kwargs={'location_id': location_id})

    def setUp(self):
        self.line1 = line1 = models.Line.objects.create(name='R5')
        self.station1 = station1 = models.Station.objects.create(name='Saint-Germain-en-Laye', line=line1)
        station1.register_daily_times([self.service_day], self.line1_times)

        self.line2 = line2 = models.Line.objects.create(name='R5')
        self.station2 = station2 = models.Station.objects.create(name='Saint-Germain-en-Laye', line=line2)
        station2.register_daily_times([self.service_day], self.line2_times)

        user = User.objects.create()
        self.location = models.Location.objects.create(user=user, name='Work')
        self.location.stations.add(self.station1, self.station2)

    def test_nonexistent_location_gives_404(self):
        url = self.baseurl(123)
        response = self.client.get(url)
        self.assertEquals(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEquals({'detail': 'Not found.'}, to_json(response))

    def test_all_times(self):
        url = self.baseurl()
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = to_json(response)
        self.assertEquals(len(self.line1_times) + len(self.line2_times), len(results))

    def test_invalid_date_param(self):
        url = self.baseurl() + '?date=malformed'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected = {
            'date': ['Enter a valid date/time.']
        }
        self.assertEquals(expected, to_json(response))

    def test_invalid_time_param(self):
        url = self.baseurl() + '?time=malformed'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)

        expected = {
            'time': ['Enter a valid time.']
        }
        self.assertEquals(expected, to_json(response))

    def test_all_times_on_service_day_by_date(self):
        url = self.baseurl() + '?date=' + self.service_datestr
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        sorted_times = sorted(self.line1_times + self.line2_times)
        self.assertEquals(sorted_times, to_times(to_json(response)))

    def test_no_times_on_nonservice_day_by_date(self):
        url = self.baseurl() + '?date=' + self.nonservice_datestr
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], to_json(response))

    def test_all_times_on_service_day_by_time(self):
        everyday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.station1.register_daily_times(everyday, self.line2_times)
        url = self.baseurl() + '?time=00:00'

        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.line2_times, to_times(to_json(response)))

    def test_no_times_on_nonservice_day_by_time(self):
        self.station1.dailyschedule_set.all().delete()
        url = self.baseurl() + '?time=00:00'

        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], to_times(to_json(response)))

    def test_times_after_6pm_by_date(self):
        url = self.baseurl() + '?date=' + self.service_datestr + ' 18:00'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.line2_times[3:], to_times(to_json(response)))

    def test_times_after_6pm_by_time(self):
        everyday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.station1.register_daily_times(everyday, self.line2_times)
        url = self.baseurl() + '?time=18:00'
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(self.line2_times[3:], to_times(to_json(response)))


class LineTestCase(APITestCase):
    def test_no_lines(self):
        url = reverse('line-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], json.loads(response.content.decode()))

    def test_one_station(self):
        line = models.Line.objects.create(name='R5')

        url = reverse('line-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = json.loads(response.content.decode())
        self.assertEquals(1, len(results))

        expected = [
            {
                'name': line.name,
                'url': TESTSERVER_URL + reverse('line-detail', kwargs={'pk': line.id})
            }
        ]
        self.assertEquals(expected, results)


class StationTimesFormTestCase(TestCase):
    def test_valid_parameterless(self):
        form = views.StationTimesForm({})
        self.assertTrue(form.is_valid())
        self.assertTrue('date' not in form.data)
        self.assertIsNone(form.cleaned_data['date'])
        self.assertTrue('time' not in form.data)
        self.assertIsNone(form.cleaned_data['time'])

    def test_invalid_malformed_date(self):
        form = views.StationTimesForm({'date': 'malformed'})
        self.assertFalse(form.is_valid())

    def test_valid_empty_date(self):
        form = views.StationTimesForm({'date': ''})
        self.assertTrue(form.is_valid())
        self.assertEquals('', form.data['date'])
        self.assertIsNone(form.cleaned_data['date'])

    def test_valid_date_as_ymd(self):
        datestr = '2016-01-09'
        form = views.StationTimesForm({'date': datestr})
        self.assertTrue(form.is_valid())
        self.assertEquals(datestr, form.data['date'])

    def test_valid_date_as_datetime(self):
        # note: valid json format would be this:
        # form = views.StationTimesForm({'date': '2012-04-23T18:25:43.511Z'})
        form = views.StationTimesForm({'date': '2012-04-23 18:25:43.511'})
        self.assertTrue(form.is_valid())

    def test_invalid_malformed_time(self):
        form = views.StationTimesForm({'time': 'malformed'})
        self.assertFalse(form.is_valid())

    def test_valid_empty_time(self):
        form = views.StationTimesForm({'time': ''})
        self.assertTrue(form.is_valid())
        self.assertEquals('', form.data['time'])
        self.assertIsNone(form.cleaned_data['time'])

    def test_valid_time_as_hh_mm(self):
        timestr = '10:21'
        form = views.StationTimesForm({'time': timestr})
        self.assertTrue(form.is_valid())
        self.assertEquals(timestr, form.data['time'])
        self.assertEquals(time(10, 21), form.cleaned_data['time'])

    def test_parse_date_with_no_date_no_time_gives_none(self):
        form = views.StationTimesForm({})
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.parse_date())

    def test_parse_date_with_empty_date_gives_now_with_time(self):
        date = timezone.now()
        form = views.StationTimesForm({'date': ''})
        self.assertTrue(form.is_valid())
        self.assertLessEqual(abs(form.parse_date() - date), timedelta(minutes=1))

    def test_parse_date_with_date_gives_date(self):
        date = timezone.now()
        form = views.StationTimesForm({'date': date})
        self.assertTrue(form.is_valid())
        self.assertEquals(date, form.parse_date())

    def test_parse_date_with_time_gives_now_with_time(self):
        t = time(12, 34)
        date = timezone.now().replace(hour=t.hour, minute=t.minute)
        form = views.StationTimesForm({'time': t})
        self.assertTrue(form.is_valid())
        self.assertLessEqual(abs(form.parse_date() - date), timedelta(minutes=1))

    def test_parse_date_with_date_and_time_gives_date_with_time(self):
        t = time(12, 34)
        date = timezone.now().replace(year=2016, month=1, day=9)
        form = views.StationTimesForm({'date': date, 'time': t})
        date = date.replace(hour=t.hour, minute=t.minute)
        self.assertTrue(form.is_valid())
        self.assertLessEqual(abs(form.parse_date() - date), timedelta(minutes=1))
