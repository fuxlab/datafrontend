from django.core.management.base import BaseCommand, CommandError
from images.tasks.image_process import update_size


class Command(BaseCommand):
    
    help = 'process image information'

    def add_arguments(self, parser):
        parser.add_argument('commands', nargs='+', type=str)

    def handle(self, *args, **options):
        commands = options['commands']

        if 'sizes' in commands:
            update_size.now()
            self.stdout.write(self.style.SUCCESS('Successfully executed create_annotation_boundingbox_conflicts'))
