from django.core.management.base import BaseCommand, CommandError
from lines import models


class Command(BaseCommand):
    help = 'Manage daily schedule'

    def add_arguments(self, parser):
        parser.add_argument('station-id')
        parser.add_argument('--days', '-d', nargs='+',
                            help='List of days, for example: Sat Sun weekdays')
        parser.add_argument('--times', '-t', nargs='+',
                            help='List of times, for example: 07:10 08:10')

    def handle(self, *args, **options):
        station_id = options['station-id']
        try:
            station = models.Station.objects.get(pk=station_id)
        except models.Station.DoesNotExist:
            raise CommandError('Station "{}" does not exist'.format(station_id))

        if not options['days'] or not options['times']:
            raise CommandError('You must specify both days and times to register')

        station.register_daily_times(options['days'], options['times'])
