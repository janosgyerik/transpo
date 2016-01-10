import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.datetime_safe import time
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
        datestr = '2016-01-10'
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


# TODO
# request = self.factory.get('/api/v1/stations/:id/times?date=')
# request = self.factory.get('/api/v1/users/:id/locations')
# request = self.factory.get('/api/v1/users/:id/locations/:id')
# request = self.factory.get('/api/v1/users/:id/locations/:id/times')
# request = self.factory.get('/api/v1/users/:id/locations/:id/times?date=')
