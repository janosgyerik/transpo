from django.core.management.base import BaseCommand, CommandError
from lines import models


class Command(BaseCommand):
    help = 'Manage locations'

    def add_arguments(self, parser):
        parser.add_argument('--user-id', '-u', type=int)
        parser.add_argument('--station-id', '-s', nargs='+', type=int,
                            help='List of stations ids')
        parser.add_argument('--create', '-c',
                            help='Create location (with specified name, user, stations)')
        parser.add_argument('--delete',
                            help='Delete location with specified id')
        parser.add_argument('--list', '-l', action='store_true',
                            help='List locations')

    def handle(self, *args, **options):
        if options['create']:
            self.create_location(options)
        elif options['delete']:
            self.delete_location(options)
        else:
            self.list_locations()

    def create_location(self, options):
        if not options['user_id'] or not options['station_id']:
            raise CommandError('you must specify both user id and station ids')

        user_id = options['user_id']
        try:
            user = models.User.objects.get(pk=user_id)
        except models.User.DoesNotExist:
            raise CommandError('user does not exist with id: {}'.format(user_id))

        stations = models.Station.objects.filter(id__in=options['station_id'])

        location = models.Location.objects.create(user=user, name=options['create'])
        for station in stations:
            location.stations.add(station)

    def delete_location(self, options):
        models.Location.objects.get(pk=options['delete']).delete()

    def list_locations(self):
        for location in models.Location.objects.all():
            self.stdout.write('{}: {}'.format(location.id, location))
