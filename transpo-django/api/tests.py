import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lines import models


class StationsTestCase(APITestCase):
    def test_no_stations(self):
        url = reverse('station-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals([], json.loads(response.content.decode()))

    def test_one_station(self):
        station_name = 'Saint-Germain-en-Laye'

        line = models.Line.objects.create(name='R5')
        station = models.Station.objects.create(name=station_name, line=line)

        url = reverse('station-list')
        response = self.client.get(url)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        results = json.loads(response.content.decode())
        self.assertEquals(1, len(results))

        expected = [
            {
                'name': station_name,
                'id': station.id,
                'line': line.id,
            }
        ]
        self.assertEquals(expected, results)

    def todo(self):
        pass
        # request = self.factory.get('/api/v1/lines')
        # request = self.factory.get('/api/v1/stations/:id/times')
        # request = self.factory.get('/api/v1/stations/:id/times?date=')
        # request = self.factory.get('/api/v1/users/:id/locations')
        # request = self.factory.get('/api/v1/users/:id/locations/:id')
        # request = self.factory.get('/api/v1/users/:id/locations/:id/times')
        # request = self.factory.get('/api/v1/users/:id/locations/:id/times?date=')
