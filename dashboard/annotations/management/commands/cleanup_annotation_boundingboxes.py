from django.core.management.base import BaseCommand, CommandError
from annotations.tasks.cleanup import cleanup_annotation_boundingboxes


class Command(BaseCommand):
    
    help = 'searches for 100% overlapping boundingboxes and delete clones'

    def handle(self, *args, **options):
        
        result_count = cleanup_annotation_boundingboxes.now()

        self.stdout.write(self.style.SUCCESS('Successfully deleted %s annotation_boundingboxes clones.' % (result_count)))