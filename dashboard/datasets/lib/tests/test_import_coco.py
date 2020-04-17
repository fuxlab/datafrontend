import os, copy

from django.test import TestCase, override_settings, Client

from datasets.lib import ImportCoco

from projects.models import Project
from datasets.models import Dataset
from images.models import Image
from categories.models import Category
from annotations.models import Annotation

class TestApiDatasets(TestCase):


    correct_json_data = {
        'info': { 'keys': 'value' },
        'images': [
            { 'id': 1, 'file_name': 'myfile.jpg', 'license': 5, 'coco_url': 'https://remoteurl.com/file.jpg' }
        ],
        'annotations': [
            { 'id': 2, 'image_id': 1, 'category_id': 3 }
        ],
        'categories': [
            { 'id': 3, 'name': 'mycat'}
        ],
        'not_known_key': [
            { 'id': 4, 'name': 'not known'}
        ],
        'licenses': [
            { 'id': 5, 'name': 'known license'}
        ]
    }

    def setUp(self):
        self.project = Project.objects.create(name='Project')
        self.dataset = Dataset.objects.create(name='Dataset', project=self.project)


    def test_read_json(self):
        subject = ImportCoco(self.dataset)
        result = subject.read_file(os.path.join('datasets/tests/data/coco', 'coco_default.json'))
        self.assertTrue(result)
        
        self.assertEqual(len(subject.data['images']), 2)
        self.assertEqual(len(subject.data['annotations']), 1)
        self.assertEqual(len(subject.data['categories']), 1)
        self.assertEqual(len(subject.data['licenses']), 1)


    def test_read_json_missing(self):
        subject = ImportCoco(self.dataset)
        result = subject.read_file(os.path.join('datasets/tests/data/coco', 'no_coco_default.json'))
        self.assertFalse(result)


    def test_convert_and_filter(self):
        test_json_data = self.correct_json_data
        test_json_data['not_known_key'] = [
            { 'id': 4, 'name': 'not known'}
        ]

        subject = ImportCoco(self.dataset)
        result = subject.convert(test_json_data)

        self.assertEqual(list(result.keys()).sort(), ['info', 'images', 'annotations', 'categories', 'licenses'].sort())
        
        self.assertEqual(list(result['images'].keys()), [ 1 ])
        self.assertEqual(list(result['annotations'].keys()), [ 2 ])
        self.assertEqual(list(result['categories'].keys()), [ 3 ])
        self.assertEqual(list(result['licenses'].keys()), [ 5 ])

        self.assertEqual(result['images'][1], test_json_data['images'][0])


    def _incorrect_data(self):
        incorrect_json_data = self.correct_json_data
        incorrect_json_data['annotations'].append({ 'id': 9, 'image_id': 2, 'category_id': 10})
        incorrect_json_data['categories'].append({ 'id': 10, 'name': 'not used' })
        incorrect_json_data['licenses'].append({ 'id': 11, 'name': 'not used' })
        return incorrect_json_data


    def test_import_ids(self):
        '''
        we only need to import stuff, that belongs to defined images
        so we can ignore the rest
        '''
        subject = ImportCoco(self.dataset)
        subject.data = subject.convert(self._incorrect_data())
        result = subject.import_ids()
        
        self.assertEqual(result['images'], [ 1 ])
        self.assertEqual(result['annotations'], [ 2 ])
        self.assertEqual(result['categories'], [ 3 ])
        self.assertEqual(result['licenses'], [ 5 ])


    def test_stats_cleaned(self):
        '''
        we only need to import stuff, that belongs to defined images
        so we can ignore the rest
        '''
        subject = ImportCoco(self.dataset)
        subject.data = subject.convert(self._incorrect_data())
        result = subject.stats()

        self.assertEqual(result, {
            'images': 1,
            'images_all': 1,
            'annotations': 1,
            'annotations_all': 2,
            'categories': 1,
            'categories_all': 2,
            'licenses': 1,
            'licenses_all': 2
        })


    def test_convert_image(self):
        '''
        the url should be set with the most relevant information available
        '''
        image_data = {
            'id': 1,
            'file_name': 'myfile.jpg',
            'license': 5,
            'url': 'https://remoteurl.com/file1.jpg',
            'coco_url': 'https://remoteurl.com/file2.jpg',
            'flickr_url': 'https://remoteurl.com/file3.jpg'
        }
        subject = ImportCoco(self.dataset)
        result = subject.convert_image_data(image_data)

        self.assertEqual(result['url'], 'https://remoteurl.com/file1.jpg')

        image_data['url'] = None
        result = subject.convert_image_data(image_data)
        self.assertEqual(result['url'], 'https://remoteurl.com/file2.jpg')

        image_data['coco_url'] = None
        result = subject.convert_image_data(image_data)
        self.assertEqual(result['url'], 'https://remoteurl.com/file3.jpg')


    def test_save(self):
        '''
        we only need to import stuff, that belongs to defined images
        so we can ignore the rest
        '''
        subject = ImportCoco(self.dataset)
        subject.data = subject.convert(self.correct_json_data)
        subject.save()

        result_i = [ image.identifier for image in Image.objects.all() ]
        expected_i = [ str(image['id']) for image in self.correct_json_data['images']]
        self.assertEqual(expected_i, result_i)

        result_c = [ category.identifier for category in Category.objects.all() ]
        expected_c = [ str(category['id']) for category in self.correct_json_data['categories']]
        self.assertEqual(expected_i, result_i)


    def test_save_annotation(self):
        '''
        test correct bbox conversion
        '''
        import copy
        subject = ImportCoco(self.dataset)
        
        # add boundingbox [x,y,width,height]
        import_data = copy.deepcopy(self.correct_json_data)
        import_data['annotations'].append({
            'id': 1000, 'image_id': 1, 'category_id': 3,
        })
        subject.data = subject.convert(import_data)
        subject.save()

        result_anno = Annotation.objects.all()[1]
        self.assertEqual(result_anno.identifier, '1000')
        self.assertEqual(result_anno.category.identifier, '3')
        self.assertEqual(result_anno.image.identifier, '1')


    def test_save_bbox(self):
        '''
        test correct bbox conversion
        '''
        import copy
        subject = ImportCoco(self.dataset)
        
        # add boundingbox [x,y,width,height]
        import_data = copy.deepcopy(self.correct_json_data)
        import_data['annotations'].append({
            'id': 1001, 'image_id': 1, 'category_id': 3,
            'bbox': [100, 100, 100, 100],
            'iscrowd': True
        })
        subject.data = subject.convert(import_data)
        subject.save()

        result_anno_bbox = Annotation.boundingbox_objects.all()[0]
        self.assertEqual(result_anno_bbox.identifier, '1001')
        self.assertEqual(result_anno_bbox.category.identifier, '3')
        self.assertEqual(result_anno_bbox.image.identifier, '1')
        self.assertEqual(result_anno_bbox.x_min, 100)
        self.assertEqual(result_anno_bbox.y_min, 100)
        self.assertEqual(result_anno_bbox.x_max, 200)
        self.assertEqual(result_anno_bbox.y_max, 200)
        self.assertEqual(result_anno_bbox.is_crowd, True)


    def test_save_segmentation(self):
        '''
        test correct bbox conversion
        '''
        subject = ImportCoco(self.dataset)
        
        # add boundingbox [x,y,width,height]
        import_data = copy.deepcopy(self.correct_json_data)
        import_data['annotations'].append({
            'id': 1002, 'image_id': 1, 'category_id': 3,
            'segmentation': [[10,10,20,10,20,20,10,20]],
            'mask': 'somestring',
            'iscrowd': True
        })
        subject.data = subject.convert(import_data)
        subject.save()

        result_anno_seg = Annotation.segmentation_objects.all()[0]
        self.assertEqual(result_anno_seg.identifier, '1002')
        self.assertEqual(result_anno_seg.category.identifier, '3')
        self.assertEqual(result_anno_seg.image.identifier, '1')
        self.assertEqual(result_anno_seg.segmentation, [[10,10,20,10,20,20,10,20]])
        self.assertEqual(result_anno_seg.mask, 'somestring')


        self.assertEqual(result_anno_seg.is_crowd, True)


    def xtest_read_real_json(self):
        '''
        references one one file of coco2017 to see if big imports cause any troule
        if they do, try to increase memory max setting in docker first!
        '''
        import time

        subject = ImportCoco(self.dataset)
        
        start_time = time.time()
        subject.read_file(os.path.join('/data/coco2017', 'instances_train2017.json'))
        print("--- %s seconds for read_file ---" % (time.time() - start_time))
        
        start_time = time.time()
        print(subject.stats())
        print("--- %s seconds for stats ---" % (time.time() - start_time))
        
        start_time = time.time()
        subject.save()
        print("--- %s seconds for save ---" % (time.time() - start_time))

        print(Annotation.objects.count())
        print(Annotation.boundingbox_objects.count())
        print(Annotation.segmentation_objects.count())
