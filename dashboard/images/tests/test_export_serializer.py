from django.test import TestCase

from images.serializers.export import ExportSerializer

class TestExportSerializer(TestCase):


    def test_basic_serialization(self):
        filter_params = {
            'dataset': [ 2 ]
        }
        
        data = {
            'id': 1,
            'dataset_id': 2,
        }

        serializer = ExportSerializer(data, filter_params=filter_params)
        self.assertEqual(serializer.data, {
            'id': '1',
            'type': 'image',
            'url': '/api/image/1.png',
            'image': '/api/image/1.png',
            'category': 2,
        })


    def test_annotation_serialization(self):
        filter_params = {
            'type': 'annotation',
            'category': [ 3 ]
        }
        
        data = {
            'id': 1,
            'annotation__id': 2,
            'annotation__category_id': 3,
        }

        serializer = ExportSerializer(data, filter_params=filter_params)
        self.assertEqual(serializer.data, {
            'id': '1-2',
            'type': 'annotation',
            'url': '/api/image/1.png',
            'image': '/api/image/1.png',
            'category': 3,
        })

    
    def test_boundingbox_serialization(self):
        filter_params = {
            'type': 'boundingbox',
            'category': [ 3 ]
        }
        
        data = {
            'id': 1,
            'annotationboundingbox__id': 2,
            'annotationboundingbox__category_id': 3,
        }

        serializer = ExportSerializer(data, filter_params=filter_params)
        self.assertEqual(serializer.data, {
            'id': '1-2',
            'type': 'boundingbox',
            'url': '/api/image/boundingbox_crop/2.png',
            'image': '/api/image/1.png',
            'category': 3,
        })


    def test_segmentation_serialization(self):
        filter_params = {
            'type': 'segmentation',
            'category': [ 3 ]
        }
        
        data = {
            'id': 1,
            'annotationsegmentation__id': 2,
            'annotationsegmentation__category_id': 3,
        }

        serializer = ExportSerializer(data, filter_params=filter_params)
        self.assertEqual(serializer.data, {
            'id': '1-2',
            'type': 'segmentation',
            'url': '/api/image/segmentation_crop/2.png',
            'image': '/api/image/1.png',
            'category': 3,
        })