from django.test import TestCase, override_settings
from tests.lib.file_handling import test_create_files, test_delete_folders

from projects.models import Project
from datasets.models import Dataset
from images.models import Image

from datasets.tasks.init_folder import init_folder_task

test_settings = override_settings(
    DATAFRONTEND = {
        'DATA_PATH': 'datasets/tests/data'
    }
)


class TestTasksInitFolder(TestCase):


    def setUp(self):
        
        self.data_path = 'datasets/tests/data/testdataset1'
        self.files = [
            self.data_path + '/testfile1.fake.jpg',
            self.data_path + '/folder11/testfile11.fake.jpg',
        ]
        test_create_files(self.files)

        self.project = Project.objects.create(name='Testproject 1')
        self.dataset = Dataset.objects.create(name='Testdataset 1', identifier='testdataset1', project=self.project)


    def tearDown(self):
        test_delete_folders([ self.data_path ])


    @test_settings
    def test_function_call_non_recursive(self):
        '''
        note: it doesn't care about existing subfolders!
        '''
        init_folder_task.now(self.dataset.id)

        image_paths = [image.path for image in Image.objects.all()]

        self.assertEqual(image_paths, [
            'testdataset1/testfile1.fake.jpg'
        ])
