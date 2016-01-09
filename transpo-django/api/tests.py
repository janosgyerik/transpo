import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lines import models

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

# TODO
# request = self.factory.get('/api/v1/stations/:id/times?date=')
# request = self.factory.get('/api/v1/users/:id/locations')
# request = self.factory.get('/api/v1/users/:id/locations/:id')
# request = self.factory.get('/api/v1/users/:id/locations/:id/times')
# request = self.factory.get('/api/v1/users/:id/locations/:id/times?date=')
