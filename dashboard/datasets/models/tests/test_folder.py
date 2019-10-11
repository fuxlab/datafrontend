from django.test import TestCase
from tests.lib.file_handling import test_create_files, test_delete_folders

from datasets.models import Folder


class TestModelsFolder(TestCase):


    def setUp(self):
        self.data_path = 'datasets/tests/data/folder1'
        test_create_files([
            self.data_path + '/testfile1.fake.jpg',
            self.data_path + '/folder11/testfile11.fake.jpg',
            self.data_path + '/folder11/testfile12.fake.png',
            self.data_path + '/folder11/testfile13.txt',
            self.data_path + '/folder11/folder111/testfile111.fake.jpg'
        ])


    def tearDown(self):
        test_delete_folders([self.data_path])
        

    def test_all(self):
        path='datasets/tests/data/'
        result = Folder.all(path)

        self.assertEqual(['folder1'], result)


    def test_files(self):
        path='datasets/tests/data/folder1/folder11'
        result = Folder.files(path, extensions=[])

        self.assertEqual(sorted(['testfile11.fake.jpg', 'testfile12.fake.png', 'testfile13.txt']), sorted(result))


    def test_files_only_some(self):
        path='datasets/tests/data/folder1/folder11'
        result = Folder.files(path, extensions=['.png', 'jpg'])

        self.assertEqual(['testfile11.fake.jpg', 'testfile12.fake.png'], result)


    def test_files_dataset(self):
        path='datasets/tests/data'
        result = Folder.files_dataset(path)
        
        self.assertEqual([
            [ path + '/folder1/testfile1.fake.jpg', 'data_folder1' ],
            [ path + '/folder1/folder11/testfile11.fake.jpg', 'data_folder1_folder11' ],
            [ path + '/folder1/folder11/testfile12.fake.png', 'data_folder1_folder11' ],
            [ path + '/folder1/folder11/folder111/testfile111.fake.jpg', 'data_folder1_folder11_folder111' ],
        ], result)
