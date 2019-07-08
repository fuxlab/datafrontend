from rest_framework import permissions
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models.functions import Concat
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
            for dataset in filter_params['dataset']:
                q_objects.add(Q(dataset=int(dataset)), Q.OR)

        if 'category' in filter_params:
            for category in filter_params['category']:
                
                if 'type' in filter_params and filter_params['type'] != 'all':
                    if filter_params['type'] == 'boundingbox':
                        q_objects.add(Q(annotationboundingbox__category_id=int(category)), Q.AND)

                    if filter_params['type'] == 'segmentation':
                        q_objects.add(Q(annotationsegmentation__category_id=int(category)), Q.AND)
                else:
                    q_objects.add(
                        (Q(annotation__category=int(category)) |
                        Q(annotationboundingbox__category=int(category)) |
                        Q(annotationsegmentation__category=int(category))), Q.OR)
    
        return q_objects


    def queryset(self, filter_params):
        '''
        queryset based on filter params
        '''
        
        q_objects = self.apply_filter(filter_params)
        
        if len(q_objects) == 0:
            return []

        return Image.objects.filter(q_objects).values_list(*ExportSerializer.queryset_fields(filter_params)).distinct('id', 'annotationboundingbox__id', 'annotationsegmentation__id')


    def format_line(self, data, filter_params):
        '''
        
        '''
        fields = ExportSerializer.queryset_fields(filter_params)
        if 'category' in filter_params:
            if data[fields.index('annotation__id')] is not None:
                # annotation data
                return [
                    '/api/image/%s.png' % (data[fields.index('id')]),
                    0,
                    0,
                    data[fields.index('id')],
                    data[4]
                ]
            elif data[fields.index('annotationboundingbox__id')] is not None:
                # boundingbox data
                return [
                    '/api/image/boundingbox_crop/%s.png' % (data[fields.index('annotationboundingbox__id')]),
                    0,
                    0,
                    data[fields.index('id')],
                    data[fields.index('annotationboundingbox__category_id')],
                    data[fields.index('annotationboundingbox__x_min')],
                    data[fields.index('annotationboundingbox__x_max')],
                    data[fields.index('annotationboundingbox__y_min')],
                    data[fields.index('annotationboundingbox__y_max')],
                ]
            elif data[fields.index('annotationsegmentation__id')] is not None:
                # segmentation data
                return [
                    '/api/image/segmentation_crop/%s.png' % (data[fields.index('annotationsegmentation__id')]),
                    0,
                    0,
                    data[fields.index('id')],
                    data[fields.index('annotationsegmentation__category_id')],
                    data[fields.index('annotationsegmentation__mask')],
                ]
        else:
            return [
                '/api/image/%s.png' % (data[fields.index('id')]),
                0,
                0,
                data[fields.index('id')],
                data[1]
            ]


    def query_export(self, filter_params):
        '''
        build raw data
        '''
        images = []
        for result_data in self.queryset(filter_params).all():
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

