from django.core.management.base import BaseCommand, CommandError
from lines import models


class Command(BaseCommand):
    help = 'Manage stations'

    def add_arguments(self, parser):
        parser.add_argument('--create', metavar='line:name',
                            help='Create station on specified line')

    def handle(self, *args, **options):
        line_name_option = options['create']
        if line_name_option:
            try:
                line_name, station_name = options['create'].split(':')
            except ValueError as e:
                raise CommandError('could not parse line:name format: {}\n  {}'.format(line_name_option, e))

            try:
                line = models.Line.objects.get(name=line_name)
            except models.Line.DoesNotExist:
                raise CommandError('No Line with this name: {}'.format(line_name))

            station = models.Station.objects.create(name=station_name, line=line)
            self.print_station(station)

        else:
            for station in models.Station.objects.all():
                self.print_station(station)

    def print_station(self, station):
        self.stdout.write('{}: {}'.format(station.id, station))
