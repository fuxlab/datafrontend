from django.test import TestCase

from projects.models import Project
from images.models import Image
from datasets.models import Dataset
from categories.models import Category

from images.api import ImageExport

class TestImagesApiExport(TestCase):


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

