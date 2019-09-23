import json

from datasets.models import Folder
from datasets.models import Dataset

from rest_framework.views import APIView
from rest_framework.response import Response


class FolderView(APIView):


    def get(self, request):
        '''
        return list of all not used folders
        '''
        folders = Folder.all()
        dataset_pathes = [ d.identifier for d in Dataset.objects.all() ]
        data = []
        for folder in folders:
            
            if folder in dataset_pathes:
                continue
            
            data.append({
                'id': folder,
                'name': folder
            })

        return Response(data)
