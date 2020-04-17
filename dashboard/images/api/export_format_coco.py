import json
import datetime

class ExportFormatCoco:
    '''
    convert a annotations into json-coco
    '''

    def __init__(self, annotations, export_params):
        self.annotations = annotations
        self.export_params = export_params

        self.export_params['type'] = self.export_params.get('type', 'all')
        self.export_params['format'] = self.export_params.get('format', 'jpg')

        self.export_params['size'] = False
        if 'size' in export_params and export_params['size'] is not False:
            self.export_params['size'] = tuple(export_params['size'].split('x'))

        return None


    def make_object(self):
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

        result_images = []
        result_images_ids = []

        result_categories = []
        result_category_ids = []

        result_annotations = []
        
        now_time = str(datetime.datetime.now())
        now_date = str(datetime.datetime.today().strftime('%Y/%m/%d'))
        now_year = int(datetime.datetime.today().strftime('%Y'))
        
        for annotation in self.annotations:

            height = annotation.image.height
            width = annotation.image.width
            file_name = annotation.image.name

            if self.export_params['size'] is not False:
                width = int(self.export_params['size'][0])
                height = int(self.export_params['size'][1])
                file_name = '%s?resize=%sx%s' % (file_name, width, height)
                
            if annotation.image.id not in result_images_ids:

                result_images.append({
                    'id': annotation.image.id,
                    'license': 1,
                    'file_name': file_name,
                    'height': height,
                    'width': width,
                    'date_captured': now_time,
                })
                result_images_ids.append(annotation.image.id)
            
            result_annotation = {
                'id': annotation.id,
                'image_id': annotation.image.id,
                'category_id': annotation.category.id
            }

            if self.export_params['type'] in ['all', 'boundingbox', 'segmentation']:
                result_annotation['bbox'] = [ annotation.x_min, annotation.y_min, annotation.width, annotation.height ]
                result_annotation['area'] = annotation.area
                result_annotation['iscrowd'] = annotation.is_crowd

            if self.export_params['type'] in ['all', 'segmentation']:
                result_annotation['segmentation'] = annotation.segmentation
                result_annotation['mask'] = annotation.mask

            
            result_annotations.append(result_annotation)

            if annotation.category.id not in result_category_ids:
                result_category_ids.append(annotation.category.id)
                
                result_categories.append({
                    'supercategory': '',
                    'id': annotation.category.id,
                    'name': annotation.category.name
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
            'images': result_images,
            'annotations': result_annotations,
            'categories': result_categories
        }
        return data


    def to_string(self):
        data = self.make_object()
        return json.dumps(data)
