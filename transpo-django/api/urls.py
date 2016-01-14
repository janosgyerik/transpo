from django.conf.urls import url, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'lines', views.LineViewSet)
router.register(r'stations', views.StationViewSet)
router.register(r'stations/(?P<station_id>[^/.]+)/times', views.StationTimesViewSet, base_name='station-times')
router.register(r'locations', views.LocationViewSet)
router.register(r'locations/(?P<location_id>[^/.]+)/times', views.LocationTimesViewSet, base_name='location-times')
router.register(r'dailyschedule', views.DailyScheduleViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
