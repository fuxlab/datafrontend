from django.core.management.base import BaseCommand, CommandError
from tools.tasks.conflicts import create_annotation_boundingbox_conflicts


class Command(BaseCommand):
    
    help = 'runs the runner to search for conflicts'

    def add_arguments(self, parser):
        parser.add_argument('commands', nargs='+', type=str)

    def handle(self, *args, **options):
        commands = options['commands']

        if 'boundingboxes' in commands:
            create_annotation_boundingbox_conflicts.now()
            self.stdout.write(self.style.SUCCESS('Successfully executed create_annotation_boundingbox_conflicts'))