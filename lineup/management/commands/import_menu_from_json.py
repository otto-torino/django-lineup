# import the logging library
import logging
import os

from django.core.management.base import BaseCommand, CommandError

from lineup.models import MenuItem

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Imports a menu tree from a json file'

    def add_arguments(self, parser):
        parser.add_argument('json_path', type=str)

    def handle(self, *args, **options):
        path = options['json_path']
        if not os.path.isfile(path):
            raise CommandError('File %s does not exist' % path)

        # read file
        with open(path, 'r') as json_file:
            json_data = json_file.read()

        if json_data:
            try:
                MenuItem.from_json(json_data)
                self.stdout.write(self.style.SUCCESS('Successfully imported menu'))
            except Exception as e:
                raise CommandError('Cannot import menu: %s' % str(e))
        else:
            raise CommandError('File %s is empty' % path)
