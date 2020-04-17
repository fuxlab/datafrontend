from django.test import TestCase
from background_task.models import Task
from background_task.tasks import tasks, TaskSchedule, TaskProxy

from projects.models import Project
from categories.models import Category
from datasets.models import Dataset
from images.models import Image
from annotations.models import Annotation

from tools.models import Conflict
from tools.tasks.conflicts import create_annotation_boundingbox_conflicts


class TestToolsTasksConflicts(TestCase):


    def setUp(self):
        self.project = Project.objects.create(name='Project 1')
        self.dataset = Dataset.objects.create(name='Test 1', project=self.project)
        self.category = Category.objects.create(name='Test Category 1', project=self.project)


    def test_find_annotation_boundingbox_conflicts(self):
        image1 = Image.objects.create(name='Name', url='http://images.com/img1.jpg', dataset=self.dataset, height=300, width=300)
        image2 = Image.objects.create(name='Name', url='http://images.com/img2.jpg', dataset=self.dataset, height=300, width=300)
        image3 = Image.objects.create(name='Name', url='http://images.com/img3.jpg', dataset=self.dataset, height=300, width=300)

        # overlap 1.0
        bb11 = Annotation.objects.create(image=image1, category=self.category, x_min=100, x_max=200, y_min=100, y_max=200)
        bb12 = Annotation.objects.create(image=image1, category=self.category, x_min=100, x_max=200, y_min=100, y_max=200)
       
        # overlap 1.0, 0.82, 0.82
        bb21 = Annotation.objects.create(image=image2, category=self.category, x_min=100, x_max=200, y_min=100, y_max=200)
        bb22 = Annotation.objects.create(image=image2, category=self.category, x_min=100, x_max=200, y_min=100, y_max=200)
        bb23 = Annotation.objects.create(image=image2, category=self.category, x_min=110, x_max=210, y_min=100, y_max=200)
        
        # overlap 0
        bb31  = Annotation.objects.create(image=image3, category=self.category, x_min=100, x_max=200, y_min=100, y_max=200)
        bb32  = Annotation.objects.create(image=image3, category=self.category, x_min=200, x_max=300, y_min=200, y_max=300)

        create_annotation_boundingbox_conflicts.now(threshold=0.8)
        
        conflicts = Conflict.objects.all()
        self.assertEqual(len(conflicts), 4)
        self.assertEqual([Conflict.REASON_AN_BB_DUP], list(set([item.reason for item in conflicts])))

        expected_conflicted_ids = [
            [bb21.id, bb22.id],
            [bb21.id, bb23.id],
            [bb22.id, bb23.id],
            [bb11.id, bb12.id],
        ]
        conflicted_ids = [item.affected_ids for item in conflicts]

        self.assertTrue(len(expected_conflicted_ids) == len(conflicted_ids))
        self.assertTrue(sorted(expected_conflicted_ids) == sorted(conflicted_ids))
