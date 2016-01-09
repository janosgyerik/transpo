from django.conf.urls import url, include
from rest_framework import routers
from api import views

'''
request = self.factory.get('/api/v1/stations/:id/times?date=')
request = self.factory.get('/api/v1/users/:id/locations')
request = self.factory.get('/api/v1/users/:id/locations/:id')
request = self.factory.get('/api/v1/users/:id/locations/:id/times')
request = self.factory.get('/api/v1/users/:id/locations/:id/times?date=')
'''
router = routers.DefaultRouter()
router.register(r'lines', views.LineViewSet)
router.register(r'stations', views.StationViewSet)
router.register(r'stations/(?P<station_id>[^/.]+)/times', views.StationTimesViewSet)
router.register(r'dailyschedule', views.DailyScheduleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
