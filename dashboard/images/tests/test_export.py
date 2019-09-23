from django.test import TestCase
from images.export import ImageExport

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.export import ImageExport

from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation

class TestImagesExport(TestCase):


    # best test set
    def test_return_images_with_dataset_scope(self):
        project = Project.objects.create(name='Project 1')
        
        dataset1 = Dataset.objects.create(name='Test Dataset 1', project=project)
        dataset2 = Dataset.objects.create(name='Test Dataset 2', project=project)
        dataset3 = Dataset.objects.create(name='Test Dataset 2', project=project)
        
        image1 = Image.objects.create(name='Text Image 1', url='http://url.1', dataset=dataset1)
        image2 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=dataset2)
        image3 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=dataset3)
        
        filter_params = {
            'dataset': [ dataset1.id, dataset2.id ]
        }

        view_obj = ImageExport()
        result = [ list(r.values()) for r in view_obj.query_export(filter_params) ]

        # we expect images from (dataset 1 or 2)
        # exported data should look like
        # filename, width, height, uid (image_id), class
        self.assertEqual(result[0], [image1.id, '%s.png' % (image1.id), 0, 0, image1.id, dataset1.id, 'dataset'])
        self.assertEqual(result[1], [image2.id, '%s.png' % (image2.id), 0, 0, image2.id, dataset2.id, 'dataset'])


    def test_return_images_with_category_scope(self):
        project = Project.objects.create(name='Project 1')
        
        dataset1 = Dataset.objects.create(name='Test Dataset 1', project=project)
        
        category1 = Category.objects.create(name='Category 1', project=project)
        category2 = Category.objects.create(name='Category 2', project=project)
        category3 = Category.objects.create(name='Category 3', project=project)
        
        image1 = Image.objects.create(name='Text Image 1', url='http://url.1', dataset=dataset1)
        image2 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=dataset1)
        image3 = Image.objects.create(name='Text Image 3', url='http://url.3', dataset=dataset1)

        annotation1 = Annotation.objects.create(image=image1, category=category1)
        annotation2 = AnnotationBoundingbox.objects.create(image=image2, category=category2, x_min=0.0, x_max=0.0, y_min=0.0, y_max=0.0)
        annotation3 = AnnotationSegmentation.objects.create(image=image3, category=category3, mask='mask')
        annotation4 = AnnotationSegmentation.objects.create(image=image3, category=category3, mask='mask2')

        filter_params = {
            'category': [ category1.id, category2.id ],
        }

        view_obj = ImageExport()
        result = view_obj.query_export(filter_params)

        self.assertTrue({
            'id': image1.id,
            'image_path': '%s.png' % (image1.id),
            'width': 0,
            'height': 0,
            'image_id': image1.id,
            'category_id': category1.id,
            'type': 'annotation'
        } in result)

        bb_data = [annotation2.id, 'boundingbox_%s.png' % (annotation2.id), '%s.png' % (image2.id), 0, 0, image2.id, category2.id, 0.0, 0.0, 0.0 ,0.0, 'boundingbox']
        #self.assertTrue(bb_data in result)


        filter_params = {
            'category': [ category3.id ],
            'type': 'segmentation'
        }

        view_obj = ImageExport()
        result = [ list(r.values()) for r in view_obj.query_export(filter_params) ]

        # we expect images from (category 1 or 2)
        # exported data should look like
        # filename, width, height, image_id, class_id, mask
        exp_data1 = [annotation3.id, 'segmentation_%s.png' % (annotation3.id), '%s.png' % (image3.id), 0, 0, image3.id, category3.id, 'mask', 'segmentation']
        exp_data2 = [annotation4.id, 'segmentation_%s.png' % (annotation4.id), '%s.png' % (image3.id), 0, 0, image3.id, category3.id, 'mask2', 'segmentation']
        
        self.assertEqual(len(result), 2)
        # no conflict here - file only needs to be downloaded once, so same filename is ok
        self.assertTrue(exp_data1 in result)
        self.assertTrue(exp_data2 in result)


    def test_return_boundingboxes(self):
        project = Project.objects.create(name='Project 1')
        
        dataset1 = Dataset.objects.create(name='Test Dataset 1', project=project)
        category = Category.objects.create(name='Category 1', project=project)
        
        image = Image.objects.create(name='Text Image 1', url='http://url.1', dataset=dataset1)
        image2 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=dataset1)
        image3 = Image.objects.create(name='Text Image 3', url='http://url.3', dataset=dataset1)
        
        annotation_annotation1 = Annotation.objects.create(image=image, category=category)
        annotation_boundingbox11 = AnnotationBoundingbox.objects.create(image=image, category=category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        annotation_boundingbox21 = AnnotationBoundingbox.objects.create(image=image2, category=category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        filter_params = {
            'category':[ category.id ],
            'type': 'boundingbox',
        }

        view_obj = ImageExport()
        result = [ list(r.values()) for r in view_obj.query_export(filter_params) ]

        # we expect images from from dataset2
        # exported data should look like
        # filename, width, height, image_id, class_id, xmin, xmax, ymin, ymax
        exp_data11 = [annotation_boundingbox11.id, 'boundingbox_%s.png' % (annotation_boundingbox11.id), '%s.png' % (image.id), 0, 0, image.id, category.id, 10.0, 20.0, 10.0, 20.0, 'boundingbox']
        exp_data21 = [annotation_boundingbox21.id, 'boundingbox_%s.png' % (annotation_boundingbox21.id), '%s.png' % (image2.id), 0, 0, image2.id, category.id, 10.0, 20.0, 10.0, 20.0, 'boundingbox']

        self.assertEqual(len(result), 2)
        self.assertTrue(exp_data11 in result)
        self.assertTrue(exp_data21 in result)


    def test_return_segmentation(self):
        project = Project.objects.create(name='Project 1')
        
        dataset1 = Dataset.objects.create(name='Test Dataset 1', project=project)
        dataset2 = Dataset.objects.create(name='Test Dataset 2', project=project)
        
        category = Category.objects.create(name='Category 1', project=project)
        
        image = Image.objects.create(name='Text Image 1', url='http://url.1', dataset=dataset1)
        image2 = Image.objects.create(name='Text Image 2', url='http://url.2', dataset=dataset2)
        image3 = Image.objects.create(name='Text Image 3', url='http://url.3', dataset=dataset2)
        
        annotation_annotation1 = Annotation.objects.create(image=image, category=category)
        annotation_segmentation1 = AnnotationSegmentation.objects.create(image=image2, category=category, mask='mask1')
        annotation_segmentation2 = AnnotationSegmentation.objects.create(image=image2, category=category, mask='mask2')

        filter_params = {
            'dataset': [ dataset2.id ],
            'category':[ category.id ],
            'type': 'segmentation',
        }

        view_obj = ImageExport()
        result = [ list(r.values()) for r in view_obj.query_export(filter_params) ]

        # we expect images from from dataset2
        # exported data should look like
        # filename, width, height, image_id, class_id, mask
        exp_data1 = [annotation_segmentation1.id, 'segmentation_%s.png' % (annotation_segmentation1.id), '%s.png' % (image2.id), 0, 0, image2.id, category.id, 'mask1', 'segmentation' ]
        exp_data2 = [annotation_segmentation2.id, 'segmentation_%s.png' % (annotation_segmentation2.id), '%s.png' % (image2.id), 0, 0, image2.id, category.id, 'mask2', 'segmentation' ]

        self.assertEqual(len(result), 2)
        self.assertTrue(exp_data1 in result)
        self.assertTrue(exp_data2 in result)


    def test_images_export_split_list(self):
        input_list = [ 1,2,3,4,5,6,7,8,9,10 ]
        split_str = '80_20'

        result = ImageExport.split_by_string(input_list, split_str)
        self.assertEqual(result, [[1,2,3,4,5,6,7,8], [9,10]])


    def test_images_export_split_list_unbalanced(self):
        input_list = [ 1,2,3,4,5,6,7,8,9,10 ]
        split_str = '50_30_20'

        result = ImageExport.split_by_string(input_list, split_str)
        self.assertEqual(result, [[1,2,3,4,5], [6,7,8], [9,10]])


    def test_images_list_to_csv_string(self):
        input_list = [
            ['col1','col2','[""""col3"and\'',123,'col4'],
            ['col21','col22','col23','col24'],
        ]
        
        result_str = ImageExport.list_to_csv_string(input_list)
        self.assertEqual(result_str, 'col1,col2,"[""""""""col3""and\'",123,col4\r\ncol21,col22,col23,col24\r\n')

