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
        parser.add_argument('--create', '-c', action='store_true',
                            help='Create specified days and times')
        parser.add_argument('--delete', action='store_true',
                            help='Delete specified days and times')
        parser.add_argument('--list', '-l', action='store_true',
                            help='List matching days and times')

    def handle(self, *args, **options):
        station_id = options['station-id']
        try:
            station = models.Station.objects.get(pk=station_id)
        except models.Station.DoesNotExist:
            raise CommandError('Station "{}" does not exist'.format(station_id))

        if options['create']:
            self.create_times(station, options)
        elif options['delete']:
            self.delete_times(station, options)
        else:
            self.list_times(station, options)

    @staticmethod
    def create_times(station, options):
        if not options['days'] or not options['times']:
            raise CommandError('You must specify both days and times to register')
        station.register_daily_times(options['days'], options['times'])

    @staticmethod
    def for_each_time(station, options, fun):
        times = station.dailyschedule_set.all()
        if options['days']:
            times = times.filter(day__in=options['days'])
        if options['times']:
            times = times.filter(time__in=options['times'])

        for t in times:
            fun(t)

    def delete_times(self, station, options):
        def fun(t):
            self.stdout.write('deleting time: {}'.format(t))
            t.delete()

        self.for_each_time(station, options, fun)

    def list_times(self, station, options):
        def fun(t):
            self.stdout.write('{}'.format(t))

        self.for_each_time(station, options, fun)
