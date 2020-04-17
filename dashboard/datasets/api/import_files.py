import os

from datasets.models import Folder
from datasets.models import Dataset

from rest_framework.response import Response

from django.conf import settings
from dashboard.lib.api_base import ApiBase

from datasets.tasks.import_coco import import_coco_task

class ImportFilesView(ApiBase):


    def get(self, request):
        '''
        return list of all not used folders
        '''
        filter_params = self.get_filter()

        dataset = False

        if 'dataset' in filter_params:
            dataset = Dataset.objects.get(pk=int(filter_params['dataset']))
        if not dataset:
            return Response({ 'success': False })

        data = []
        path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], dataset.identifier)
        files = Folder.files(path, ['.json'])
        for index, file in enumerate(files):
            data.append({
                'id': index,
                'file_name': file,
                'size': os.stat(os.path.join(path, file)).st_size,
                'dataset': dataset.id
            })

        return Response(data)


    def post(self, request):
        dataset = False
        if 'dataset' in request.POST:
            dataset = Dataset.objects.get(pk=int(request.POST['dataset']))
    
        if not dataset:
            return Response({ 'success': False })

        data = {}
        
        if 'file_name' in request.POST:
            file_name = request.POST['file_name']
            import_coco_task(dataset.id, file_name)

            return Response({
                'success': True
            })

        return Response({ 'success': False })
