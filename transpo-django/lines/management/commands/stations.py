from django.core.management.base import BaseCommand, CommandError
from lines import models


class Command(BaseCommand):
    help = 'Manage stations'

    def add_arguments(self, parser):
        parser.add_argument('--create', metavar='line:name',
                            help='Create station on specified line')
        parser.add_argument('--times', '-t', action='store_true',
                            help='Show times of stations')

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
            show_times = options['times']

            for station in models.Station.objects.all():
                self.print_station(station, show_times)

    def print_station(self, station, show_times=False):
        self.stdout.write('{}: {}'.format(station.id, station))
        if show_times:
            for schedule in station.dailyschedule_set.all():
                self.stdout.write('  {}'.format(schedule.day_and_time))
            self.stdout.write('')
