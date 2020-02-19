import json

from datasets.models import Dataset
from images.models import Image
from categories.models import Category
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class ImportCoco:

    '''
    definitions of keys and mappings
    '''
    keys_root = {
        'info': {
            'type': dict,
            'blank': True,
            'fields': {
                'version': 'version',
                'description': 'description',
                'contributor': 'contributor',
                'url': 'url',
                'release_date': 'year',
            }
        },
        'images': {
            'type': list,
            'blank': False,
            'fields': {
                'name': 'file_name',
                'url':'flickr_url',
            }
        },
        'annotations': {
            'type': list,
            'blank': True,
        },
        'licenses': { 'type': list, 'blank': True },
        'categories': {
            'type': list,
            'blank': True,
        },
    }


    def __init__(self, dataset):
        self.name = 'New Dataset'
        self.data = {}
        self.dataset = dataset
        return None


    def convert(self, json_data):
        '''
        make list to key, dict and filter not known key values
        '''
        data = {}
        for key, items in json_data.items():
            if key in self.keys_root.keys() and self.keys_root[key]['type'] == list:
                data[key] = { item['id'] : item for item in items }
            elif key in self.keys_root.keys():
                data[key] = items
        return data

    
    def read_file(self, file_path):
        '''
        just reading and parsing coco json file
        '''
        try:
            with open(file_path) as f:
                self.data = self.convert(json.load(f))
        except:
            return False
        return True

    
    def import_ids(self):
        '''
        cleanup not used entries
        '''
        image_ids = []
        license_ids = []
        for image_id, image in self.data['images'].items():
            image_ids.append(image['id'])
            if 'license' in image:
                license_ids.append(image['license'])

        image_ids = list(set(image_ids))
        license_ids = list(set(license_ids))

        annotation_ids = []
        category_ids = []
        for annotation_id, annotation in self.data['annotations'].items():
            if annotation['image_id'] in image_ids:
                if 'id' in annotation:
                    annotation_ids.append(annotation['id'])
                if 'category_id' in annotation:
                    category_ids.append(annotation['category_id'])

        annotation_ids = list(set(annotation_ids))
        category_ids = list(set(category_ids))
        
        return {
            'images': image_ids,
            'licenses': license_ids,
            'annotations': annotation_ids,
            'categories': category_ids,
        }


    def stats(self):
        '''
        get some stats for upload report
        '''
        stats = {}
        cleaned_ids = self.import_ids()
        for key, key_data in self.keys_root.items():
            if key in cleaned_ids:
                stats[key] = len(cleaned_ids[key])
            else:
                stats[key] = 0

            if key in self.data:
                stats[key + '_all'] = len(self.data[key])
            else:
                stats[key + '_all'] = 0

        return stats

    def convert_image_data(self, image_data):
        image_import_data = {
            'dataset': self.dataset,
            'identifier': image_data.get('id', None),
            'width': image_data.get('width', None),
            'height': image_data.get('height', None),
            'name': image_data.get('file_name', None),
            'url': None
        }
        if 'url' in image_data and bool(image_data['url'] and image_data['url'].strip()):
            image_import_data['url'] = image_data['url']
        elif 'coco_url' in image_data and bool(image_data['coco_url'] and image_data['coco_url'].strip()):
            image_import_data['url'] = image_data['coco_url']
        elif 'flickr_url' in image_data and bool(image_data['flickr_url'] and image_data['flickr_url'].strip()):
            image_import_data['url'] = image_data['flickr_url']
        return image_import_data


    def save(self):
        '''
        create database entries
        we don't need to care about duplicate ids, cause there is only one import per dataset allowed
        '''
        dataset_data = {
            'name': self.name
        }
        for db_key, data_key in self.keys_root['info']['fields'].items():
            if data_key in self.data['info']:
                self.dataset.__setattr__(db_key, self.data['info'][data_key])
        self.dataset.save()


        category_id_match = {}
        import_ids = self.import_ids()
        for category_id in import_ids['categories']:
            category_data = self.data['categories'][category_id]

            category_import_data = {
                'identifier': category_id,
                'name': category_data['name'],
                'project_id': self.dataset.project.id
            }
            category, created = Category.objects.get_or_create(**category_import_data)
            category_id_match[category_id] = category.id


        image_id_match = {}
        for image_id in import_ids['images']:
            image_import_data = self.convert_image_data(self.data['images'][image_id])
            image = Image.objects.create(**image_import_data)
            image_id_match[image_id] = image.id


        for annotation_id in import_ids['annotations']:
            annotation_data = self.data['annotations'][annotation_id]

            if 'category_id' not in annotation_data or 'image_id' not in annotation_data:
                continue

            image_id = image_id_match[annotation_data['image_id']]
            category_id = category_id_match[annotation_data['category_id']]

            if 'segmentation' in annotation_data or 'mask' in annotation_data:
                annotation_import_data = {
                    'identifier': annotation_id,
                    'image_id': image_id,
                    'category_id': category_id,
                    'is_crowd': annotation_data.get('iscrowd', False),
                    'area': annotation_data.get('area', 0),
                    
                    'mask': annotation_data.get('mask', None),
                    'segmentation': annotation_data.get('segmentation', []),                    
                }

                if 'bbox' in annotation_data and len(annotation_data['bbox']) is 4:
                    # [x,y,width,height]
                    annotation_import_data['x_min'] = annotation_data['bbox'][0]
                    annotation_import_data['x_max'] = annotation_data['bbox'][0] + annotation_data['bbox'][2]
                    annotation_import_data['y_min'] = annotation_data['bbox'][1]
                    annotation_import_data['y_max'] = annotation_data['bbox'][1] + annotation_data['bbox'][3]


                seg = AnnotationSegmentation.objects.create(**annotation_import_data)

            elif 'bbox' in annotation_data:
                if len(annotation_data['bbox']) is not 4:
                    continue
                annotation_import_data = {
                    'identifier': annotation_id,
                    'image_id': image_id,
                    'category_id': category_id,
                    'is_crowd': annotation_data.get('iscrowd', False),
                    'area': annotation_data.get('area', 0),
                    # [x,y,width,height]
                    'x_min': annotation_data['bbox'][0],
                    'x_max': annotation_data['bbox'][0] + annotation_data['bbox'][2],
                    'y_min': annotation_data['bbox'][1],
                    'y_max': annotation_data['bbox'][1] + annotation_data['bbox'][3],
                }
                AnnotationBoundingbox.objects.create(**annotation_import_data)
            
            else: # 'bbox' not in annotation_data and 'segmentation' not in annotation_data:
                annotation_import_data = {
                    'identifier': annotation_id,
                    'image_id': image_id,
                    'category_id': category_id,
                }
                Annotation.objects.create(**annotation_import_data)

        return True

