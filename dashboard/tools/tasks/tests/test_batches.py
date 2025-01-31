from django.test import TestCase
from background_task.models import Task
from background_task.tasks import tasks, TaskSchedule, TaskProxy

from projects.models import Project
from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation

from tools.models import Batch
from tools.tasks.batches import update_images_dataset, update_annotations_category, update_annotation_boundingboxes_category, update_annotation_segmentations_category


class TestAnnotationsTasksBatches(TestCase):


    def setUp(self):
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)


    def test_update_images_dataset(self):
        image1 = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        image2 = Image.objects.create(name='Name', url='http://images.com/img2.jpg', dataset=self.dataset)
        image3 = Image.objects.create(name='Name', url='http://images.com/img3.jpg', dataset=self.dataset)
        image4 = Image.objects.create(name='Name', url='http://images.com/img4.jpg', dataset=self.dataset)
        image5 = Image.objects.create(name='Name', url='http://images.com/img5.jpg', dataset=self.dataset)

        image6 = Image.objects.create(name='Name', url='http://images.com/img5.jpg', dataset=self.dataset)
        
        dataset2 = Dataset.objects.create(name='Test 2', project=self.project)
        batch = Batch.objects.create(action='update_images_dataset', params=[ [image1.id, image2.id, image3.id, image4.id, image5.id], dataset2.id] )
        self.assertEqual(batch.status, 'pending')

        changed_items = update_images_dataset.now(batch.id)
        self.assertEqual(changed_items, 5)
        self.assertEqual(Image.objects.filter(dataset=dataset2).count(), 5)

        batch = Batch.objects.get(id=batch.id)
        self.assertEqual(batch.status, 'finished')


    def test_update_annotation_category(self):
        image1 = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        image2 = Image.objects.create(name='Name', url='http://images.com/img2.jpg', dataset=self.dataset)

        bb11 = Annotation.objects.create(image=image1, category=self.category)
        bb12 = Annotation.objects.create(image=image1, category=self.category)
        bb21 = Annotation.objects.create(image=image2, category=self.category)
        bb22 = Annotation.objects.create(image=image2, category=self.category)
        bb3  = Annotation.objects.create(image=image2, category=self.category)

        category2 = Category.objects.create(name='Test Category 2', project=self.project)
        batch = Batch.objects.create(action='update_annotations_category', params=[ [bb11.id, bb12.id, bb21.id, bb22.id], category2.id] )

        changed_items = update_annotations_category.now(batch.id)
        self.assertEqual(changed_items, 4)
        self.assertEqual(Annotation.objects.filter(category=category2).count(), 4)

        batch = Batch.objects.get(id=batch.id)
        self.assertEqual(batch.status, 'finished')

    
    def test_update_annotation_boundingboxes_category(self):
        image1 = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        image2 = Image.objects.create(name='Name', url='http://images.com/img2.jpg', dataset=self.dataset)

        bb11 = Annotation.objects.create(image=image1, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        bb12 = Annotation.objects.create(image=image1, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        bb21 = Annotation.objects.create(image=image2, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        bb22 = Annotation.objects.create(image=image2, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)
        bb3  = Annotation.objects.create(image=image2, category=self.category, x_min=10.0, x_max=20.0, y_min=10.0, y_max=20.0)

        category2 = Category.objects.create(name='Test Category 2', project=self.project)
        batch = Batch.objects.create(action='update_annotation_boundingboxes_category', params=[ [bb11.id, bb12.id, bb21.id, bb22.id], category2.id] )

        changed_items = update_annotation_boundingboxes_category.now(batch.id)
        self.assertEqual(changed_items, 4)
        self.assertEqual(Annotation.boundingbox_objects.filter(category=category2).count(), 4)

        batch = Batch.objects.get(id=batch.id)
        self.assertEqual(batch.status, 'finished')


    def test_update_annotation_segmnentations_category(self):
        image1 = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset)
        image2 = Image.objects.create(name='Name', url='http://images.com/img2.jpg', dataset=self.dataset)

        bb11 = Annotation.objects.create(image=image1, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        bb12 = Annotation.objects.create(image=image1, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        bb21 = Annotation.objects.create(image=image2, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        bb22 = Annotation.objects.create(image=image2, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])
        bb3  = Annotation.objects.create(image=image2, category=self.category, segmentation=[[10,10,10,20,20,20,20,10]])

        category2 = Category.objects.create(name='Test Category 2', project=self.project)
        batch = Batch.objects.create(action='update_annotation_segmentations_category', params=[ [bb11.id, bb12.id, bb21.id, bb22.id], category2.id] )

        changed_items = update_annotation_segmentations_category.now(batch.id)
        self.assertEqual(changed_items, 4)
        self.assertEqual(Annotation.segmentation_objects.filter(category=category2).count(), 4)

        batch = Batch.objects.get(id=batch.id)
        self.assertEqual(batch.status, 'finished')
