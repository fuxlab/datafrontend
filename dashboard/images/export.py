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

from datasets.models import Dataset
from categories.models import Category

import csv, io
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


    def list_to_csv_string(lines):
        '''
        format a list to string to be saved as csv
        '''
        string = io.StringIO()
        
        for line in lines:
            writer = csv.writer(string)
            writer.writerow(line)
        
        return string.getvalue()

    def list_to_coco_string(lines, resize=None):
        '''
        format a list to string to be saved in coco format
        '''
        licenses = [
            {
                "url": "http://creativecommons.org/createLicense",
                "id": 1,
                "name": "no license given"
            }
        ]

        images = []
        images_ids = []

        categories = []
        category_ids = []

        annotations = []
        
        now_time = str(datetime.datetime.now())
        now_date = str(datetime.datetime.today().strftime('%Y/%m/%d'))
        now_year = int(datetime.datetime.today().strftime('%Y'))
        
        for line in lines:

            height = line['height']
            width = line['width']
            file_name = line['image_path']

            if resize is not None:
                width = int(resize[0])
                height = int(resize[1])
                file_name = '%s?resize=%sx%s' % (file_name, width, height)
                
            if line['image_id'] not in images_ids:
                images.append({
                    'license': 1,
                    'file_name': file_name,
                    'height': height,
                    'width': width,
                    "date_captured": now_time,
                    'id': line['image_id']
                })
            
            area = 0
            if 'x_min' in line:
                area = (((line['x_max'] - line['x_min']) * width) * ((line['y_max'] - line['y_min']) * height))

            annotation = {
                'id': line['id'],
                'image_id': line['image_id'],
                'category_id': line['category_id'],
                'area': area,
                'iscrowd': 0,
            }
            
            if 'mask' in line:
                annotation['segmentation'] = line['mask']
            
            if 'x_min' in line:
                # x, y, width, height
                annotation['bbox'] = [
                    line['x_min'] * width,
                    line['y_min'] * height,
                    (line['x_max'] - line['x_min']) * width,
                    (line['y_max'] - line['y_min']) * height,
                ]
            annotations.append(annotation)

            if line['category_id'] not in category_ids:
                category_ids.append(line['category_id'])
                if line['type'] == 'dataset':
                    name = Dataset.quick_name(line['category_id'])
                else:
                    name = Category.quick_name(line['category_id'])

                categories.append({
                    'supercategory': '',
                    'id': line['category_id'],
                    'name': name
                })

        data = {
            'info': {
                'description': 'Datafrontend export',
                'url': 'https://datafrontend.com',
                'version': '1.0',
                'year': now_year,
                'contributor': 'Datafrontend User',
                'date_created': now_date
            },
            'licenses': licenses,
            'images': images,
            'annotations': annotations,
            'categories': categories
        }

        return json.dumps(data)
    

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
            *self.queryset_fields(filter_params)
        ).annotate(
            pks=ArrayAgg(
                self.aggid(filter_params)
            )
        )

        if('max' in filter_params):
            q = q[:int(filter_params['max'])]
        return q


    def queryset_fields(self, filter_params):
        '''
        mapping for query resultset
        '''
        fields = [ 'id', 'width', 'height' ]
        if 'category' in filter_params:
            filter_type = filter_params['type'] if 'type' in filter_params else 'all'

            if filter_type == 'all':
                fields.append('annotation__id')
                fields.append('annotation__category_id')
            
            if filter_type == 'boundingbox':
                fields.append('annotationboundingbox__id')
                fields.append('annotationboundingbox__category_id')
                fields.append('annotationboundingbox__x_min')
                fields.append('annotationboundingbox__x_max')
                fields.append('annotationboundingbox__y_min')
                fields.append('annotationboundingbox__y_max')
            
            if filter_type == 'segmentation':
                fields.append('annotationsegmentation__id')
                fields.append('annotationsegmentation__category_id')
                fields.append('annotationsegmentation__mask')
            
            if filter_type == 'annotation':
                fields.append('annotation__id')
                fields.append('annotation__category_id')
        else:
            fields.append('dataset_id')

        return fields


    def format_line(self, data, filter_params):
        '''
        
        '''
        fields = self.queryset_fields(filter_params)

        if 'ext' in filter_params and filter_params['ext'] == 'jpg':
            ext = 'jpg'
        else:
            ext = 'png'

        if 'category' not in filter_params:
            return {
                'id': data['id'],
                'image_path': ('%s.%s' % (data['id'], ext)),
                'width': data['width'],
                'height': data['height'],
                'image_id': data['id'],
                'category_id': data['dataset_id'],
                'type': 'dataset',
            }

        if 'annotation__id' in data and  data['annotation__id'] is not None:
            # annotation data
            return {
                'id': data['id'],
                'image_path': ('%s.%s' % (data['id'], ext)),
                'width': data['width'],
                'height': data['height'],
                'image_id': data['id'],
                'category_id': data['annotation__category_id'],
                'type': 'annotation',
            }
        
        if 'annotationboundingbox__id' in data and data['annotationboundingbox__id'] is not None:
            # boundingbox data
            return {
                'id': data['annotationboundingbox__id'],
                'annotation_boundingbox_image_path': ('boundingbox_%s.%s' % (data['annotationboundingbox__id'], ext)),
                'image_path': ('%s.%s' % (data['id'], ext)),
                'width': data['width'],
                'height': data['height'],
                'image_id': data['id'],
                'category_id': data['annotationboundingbox__category_id'],
                'x_min': data['annotationboundingbox__x_min'],
                'x_max': data['annotationboundingbox__x_max'],
                'y_min': data['annotationboundingbox__y_min'],
                'y_max': data['annotationboundingbox__y_max'],
                'type': 'boundingbox',
            }
        
        if 'annotationsegmentation__id' in data and data['annotationsegmentation__id'] is not None:
            # segmentation data
            return {
                'id': data['annotationsegmentation__id'],
                'annotation_segmentation_image_path': ('segmentation_%s.%s' % (data['annotationsegmentation__id'], ext)),
                'image_path': ('%s.%s' % (data['id'], ext)),
                'width': data['width'],
                'height': data['height'],
                'image_id': data['id'],
                'category_id': data['annotationsegmentation__category_id'],
                'mask': data['annotationsegmentation__mask'],
                'type': 'segmentation',
            }
        return {}

    
    def query_export(self, filter_params):
        '''
        build raw data
        '''
        images = []
        for result_data in self.queryset(filter_params):
            images.append(
                self.format_line(result_data, filter_params)
            )
        return images


    def download(self, request):
        '''
        api download endpoint for zip export
        '''
        filter_params = self.get_filter()
        export_format = filter_params.get('format', 'csv')

        images = self.query_export(filter_params)
        
        if 'shuffle' in filter_params and filter_params['shuffle'] == 'yes':
            random.shuffle(images)
        
        if 'split' in filter_params:
            images_chuncks = ImageExport.split_by_string(images, filter_params['split'])
        else:
            images_chuncks = [ images ]

        resize = None
        if 'resize' in filter_params:
            resize = tuple(filter_params['resize'].split('x'))

        
        files = []
        i = 0
        for image_chunck in images_chuncks:
            
            if export_format == 'csv':
                # make list without id
                data_list = [ list(r.values())[1:] for r in image_chunck ]
                files.append({
                    'file': '%s.csv' % (chr(97 + i)),
                    'content': ImageExport.list_to_csv_string(data_list)
                })
            
            elif export_format == 'coco':
                files.append({
                    'file': '%s.json' % (chr(97 + i)),
                    'content': ImageExport.list_to_coco_string(image_chunck, resize=resize)
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

