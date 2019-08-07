from django.core.management.base import BaseCommand, CommandError
from annotations.tasks.cleanup import cleanup_annotation_boundingboxes


class Command(BaseCommand):
    
    help = 'searches for 100% overlapping boundingboxes and delete clones'
    
    def add_arguments(self, parser):
        parser.add_argument('commands', nargs='+', type=str)

    def handle(self, *args, **options):
        category_ids = []
        category_ids_string = options['commands'][0]
        
        if len(category_ids_string) > 0:
            category_ids = [x.strip() for x in category_ids_string.split(',')]
        result_count = cleanup_annotation_boundingboxes.now(category_ids)

        self.stdout.write(self.style.SUCCESS('Successfully deleted %s annotation_boundingboxes clones from %s categories.' % (result_count, ', '.join(category_ids))))