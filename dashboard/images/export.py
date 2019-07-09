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
from images.serializers.export import ExportSerializer

import csv, io
import zipfile, json

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


    def list_to_csv_string(lines):
        '''
        format a list to string to be saved as csv
        '''
        string = io.StringIO()
        
        for line in lines:
            writer = csv.writer(string)
            writer.writerow(line)
        
        return string.getvalue()
    

    def apply_filter(self, filter_params):
        '''
        build a queryset by requests filter params hash
        '''
        q_objects = Q()
        
        if 'dataset' in filter_params:
            q_ors = Q()
            for dataset in filter_params['dataset']:
                q_ors.add(Q(dataset=int(dataset)), Q.OR)
            q_objects.add(q_ors, Q.AND)
        
        if 'category' not in filter_params:
            return q_objects

        filter_type = filter_params['type'] if 'type' in filter_params else 'all'
        if filter_type == 'all':
            q_objects.add((
                Q(annotation__category__in=filter_params['category']) |
                Q(annotationboundingbox__category__in=filter_params['category']) |
                Q(annotationsegmentation__category__in=filter_params['category'])
            ),Q.AND) 
        elif filter_type == 'boundingbox':
            q_objects.add(Q(annotationboundingbox__category_id__in=filter_params['category']), Q.AND)
        elif filter_type == 'segmentation':
            q_objects.add(Q(annotationsegmentation__category_id__in=filter_params['category']), Q.AND)
        elif filter_type == 'annotation':
            q_objects.add(Q(annotation__category_id__in=filter_params['category']), Q.AND)


        return q_objects


    def apply_distinct(self, filter_params):
        filter_type = filter_params['type'] if 'type' in filter_params else 'all'
        if filter_type == 'segmentation':
            return ['id', 'annotationsegmentation__id']
        if filter_type == 'boundingbox':
            return [ 'id', 'annotationboundingbox__id']
        if filter_type == 'annotation':
            return ['id', 'annotation__id']
        return ['id', 'annotationsegmentation__id', 'annotationboundingbox__id', 'annotation__id']


    def aggid(self, filter_params):
        filter_type = filter_params['type'] if 'type' in filter_params else 'all'
        if filter_type == 'segmentation':
            return 'annotationsegmentation__id'
        if filter_type == 'boundingbox':
            return 'annotationboundingbox__id'
        if filter_type == 'annotation':
            return 'annotation__id'
        return 'id'



    def queryset(self, filter_params):
        '''
        queryset based on filter params
        '''
        
        q_objects = self.apply_filter(filter_params)
        
        if len(q_objects) == 0:
            return []

        q = Image.objects.filter(q_objects).values(
            *ExportSerializer.queryset_fields(filter_params)
        ).annotate(
            pks=ArrayAgg(
                self.aggid(filter_params)
            )
        )
        return q


    def format_line(self, data, filter_params):
        '''
        
        '''
        fields = ExportSerializer.queryset_fields(filter_params)
        if 'category' not in filter_params:
            return [
                '/api/image/%s.png' % (data['id']),
                0,
                0,
                data['id'],
                data['dataset_id']
            ]

        if 'annotation__id' in data and  data['annotation__id'] is not None:
            # annotation data
            return [
                '/api/image/%s.png' % (data['id']),
                0,
                0,
                data['id'],
                data['annotation__category_id']
            ]
        
        if 'annotationboundingbox__id' in data and data['annotationboundingbox__id'] is not None:
            # boundingbox data
            return [
                '/api/image/boundingbox_crop/%s.png' % (data['annotationboundingbox__id']),
                0,
                0,
                data['id'],
                data['annotationboundingbox__category_id'],
                data['annotationboundingbox__x_min'],
                data['annotationboundingbox__x_max'],
                data['annotationboundingbox__y_min'],
                data['annotationboundingbox__y_max'],
            ]
        
        if 'annotationsegmentation__id' in data and data['annotationsegmentation__id'] is not None:
            # segmentation data
            return [
                '/api/image/segmentation_crop/%s.png' % (data['annotationsegmentation__id']),
                0,
                0,
                data['id'],
                data['annotationsegmentation__category_id'],
                data['annotationsegmentation__mask'],
            ]


    def query_export(self, filter_params):
        '''
        build raw data
        '''
        images = []
        for result_data in self.queryset(filter_params):
            images.append(self.format_line(result_data, filter_params))

        return images


    def chunck_query(self, filter_params):
        '''
        build chuncked raw data to save to file
        '''
        images_chuncks = self.query_export(filter_params)
        
        if 'split' in filter_params:
            return ImageExport.split_by_string(images_chuncks, filter_params['split'])
        
        return [ images_chuncks ]


    def download(self, request):
        '''
        api download endpoint for zip export
        '''
        filter_params = self.get_filter()
        images_chuncks = self.chunck_query(filter_params)

        files = []
        i = 0
        for image_chunck in images_chuncks:
            files.append({
                'file': '%s.csv' % (chr(97 + i)),
                'content': ImageExport.list_to_csv_string(image_chunck)
            })
            i += 1

        zip_filename = 'output_filename.zip'
        response = HttpResponse(content_type='application/zip')
        zf = zipfile.ZipFile(response, 'w')
        
        for file in files:
            zf.writestr(file['file'], file['content'])

        response['Content-Disposition'] = 'attachment; filename=%s' % (zip_filename)
        return response


    def list(self, request):
        '''
        api entpoint for frontend
        '''
        pagination = Pagination()
        filter_params = self.get_filter()
        images = pagination.paginate_queryset(self.queryset(filter_params), request)
        serializer = ExportSerializer(images, many=True, filter_params=filter_params)
        return pagination.get_paginated_response(serializer.data)

