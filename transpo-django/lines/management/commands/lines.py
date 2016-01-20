from django.core.management.base import BaseCommand
from lines import models


class Command(BaseCommand):
    help = 'Manage lines'

    def add_arguments(self, parser):
        parser.add_argument('--create', '-c', metavar='name')
        parser.add_argument('--list', '-l', action='store_true')

    def handle(self, *args, **options):
        if options['create']:
            line = models.Line.objects.create(name=options['create'])
            self.print_line(line)
        else:
            for line in models.Line.objects.all():
                self.print_line(line)

    def print_line(self, line):
        self.stdout.write('{}'.format(line))
