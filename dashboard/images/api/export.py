from rest_framework import permissions
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models.functions import Concat
from django.contrib.postgres.aggregates import ArrayAgg

from django.db.models import Q, Value, CharField, F
from django.conf import settings
from django.http import HttpResponse

from dashboard.lib.api_base import DashboardApiBase
from dashboard.lib.pagination import Pagination

from images.models import Image
from annotations.models import Annotation

from images.api import ExportFormatCoco
from images.serializers import ExportSerializer

from datasets.models import Dataset
from categories.models import Category

import io
import datetime
import zipfile, json
import random


class ImageExport(DashboardApiBase):

    
    permission_classes = [
        permissions.AllowAny
    ]

    def percentage_split(seq, percentages):
        '''
        split a list into chuncks of different, percentage sizes
        '''
        prv = 0
        size = len(seq)
        cum_percentage = 0
        for p in percentages:
            cum_percentage += p/100
            nxt = int(cum_percentage * size)
            yield seq[prv:nxt]
            prv = nxt


    def split_by_string(result_list, split_str):
        '''
        split list by percentage presented in sting as 80_10_10
        '''
        split_sizes = list(map(int, split_str.split('_')))
        return list(ImageExport.percentage_split(result_list, split_sizes))
    

    def apply_filter(self, export_params):
        '''
        build a queryset by requests filter params hash
        '''
        q_objects = Q()
        
        if 'dataset' in export_params:
            q_ors = Q()
            for dataset in export_params['dataset']:
                q_ors.add(Q(image__dataset=int(dataset)), Q.OR)
            q_objects.add(q_ors, Q.AND)
        
        if 'category' not in export_params:
            return q_objects

        filter_type = export_params['type'] if 'type' in export_params else 'all'

        if filter_type == 'all' or filter_type == 'annotation':
            q_objects.add((
                Q(category__in=export_params['category'])
            ),Q.AND) 
        elif filter_type == 'boundingbox':
            q_objects.add(
                Q(category_id__in=export_params['category']) &
                ~Q(x_min__isnull=True)
            , Q.AND)
        elif filter_type == 'segmentation':
            q_objects.add(
                Q(category_id__in=export_params['category']) &
                ~Q(segmentation__isnull=True)
            , Q.AND)

        return q_objects


    def queryset(self, export_params):
        '''
        queryset based on filter params
        '''
        
        if 'category' not in export_params and 'dataset' not in export_params:
            return []

        q_objects = self.apply_filter(export_params)
        q = Annotation.objects.filter(q_objects)
        
        # TODO switch to db max
        if('max' in export_params):
            q = q[:int(export_params['max'])]

        return q

    
    def list(self, request):
        '''
        api entpoint with annotations for frontend
        '''
        pagination = Pagination()
        export_params = self.get_filter()
        annotations = pagination.paginate_queryset(self.queryset(export_params), request)
        serializer = ExportSerializer(annotations, many=True, export_params=export_params)
        return pagination.get_paginated_response(serializer.data)


    def single(self, annotations, export_params={}):
        '''
        api endpint for one file download
        '''
        data = []
        if export_params['format'] == 'coco':
            data = ExportFormatCoco(annotations, export_params).to_string()
        
        response = HttpResponse(data)
        response['Content-Disposition'] = 'attachment; filename=%s' % ('download_single.json')
        return response


    def multi(self, annotations, export_params={}):
        '''
        splitted and zipped result, with more than one file
        '''
        annotations_chuncks = ImageExport.split_by_string(annotations, export_params['split'])
        files = []
        for i, annotation_chunck in enumerate(annotations_chuncks):
            
            if export_params['format'] == 'coco':
                files.append({
                    'file': '%s.json' % (chr(97 + i)), # genrates a, b, c, d ... filenames
                    'content': ExportFormatCoco(annotation_chunck, export_params).to_string()
                })

        zip_filename = 'output_filename.zip'
        response = HttpResponse(content_type='application/zip')
        zf = zipfile.ZipFile(response, 'w')
        
        for file in files:
            zf.writestr(file['file'], file['content'])

        response['Content-Disposition'] = 'attachment; filename=%s' % (zip_filename)
        return response


    def download(self, request):
        '''
        api endpoint for  download multi files as zip
        '''

        export_params = self.get_filter()
        export_params['format'] = export_params.get('format', 'coco')
        export_params['type'] = export_params.get('type', 'all')

        annotations = self.queryset(export_params)
        
        if 'shuffle' in export_params and export_params['shuffle'] == 'yes':
            random.shuffle(annotations)

        if 'shuffle' in export_params and export_params['shuffle'] == 'yes':
            random.shuffle(annotations)

        if 'split' in export_params:
            return self.multi(annotations, export_params)
        
        return self.single(annotations, export_params)

