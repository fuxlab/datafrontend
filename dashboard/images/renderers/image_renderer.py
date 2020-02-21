from rest_framework import permissions, renderers, viewsets

from django.http import HttpResponse
from rest_framework.response import Response

from django.conf import settings
import os, math
from io import BytesIO

from PIL import Image as PImage
from PIL import ImageDraw
import pycocotools.mask as mask
import numpy as np

import requests
from io import BytesIO

from images.models import Image
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation

from images.renderers import PNGRenderer

class ImageRenderer(viewsets.ModelViewSet):
    
    permission_classes = [
        permissions.AllowAny
    ]
    status = 200
    
    renderer_classes = (PNGRenderer, )
    ext = 'PNG'


    def resize(self, request, img):
        if 'resize' in request.query_params:
            width, height = request.query_params['resize'].split('x')
            img = img.resize((int(width),int(height)))
        return img


    def thumbnail(self, request, format=None, id=None):
        '''
        endpoint for image thumbnail in 200x200 size
        '''
        (image, img) = self.find_and_open_image(id)

        output = BytesIO()
        img.thumbnail((200,200))
        img.save(output, format=self.ext)
        output.seek(0)
        
        return Response(output.read(), status=self.status)


    def preview(self, request, format=None, id=None):
        '''
        endpoint for image preview with maximum 800x600 size
        optional with boundingboxes, and segmentation overlay
        '''
        (image, img) = self.find_and_open_image(id)
        
        output = BytesIO()

        image_type = self.request.query_params.get('type')
        if image_type is not None:
            if image_type == 'boundingbox':
                img = self.draw_boundingbox(image, img)
            if image_type == 'segmentation':
                img = self.draw_segmentation(image, img)
        
        img.thumbnail((800,600))
        img.save(output, format=self.ext)
        output.seek(0)
        return Response(output.read(), status=self.status)


    def original(self, request, format=None, id=None):
        '''
        endpoint to render original image
        '''
        (image, img) = self.find_and_open_image(id)
        img = self.resize(request, img)

        output = BytesIO()
        img.save(output, format=self.ext)
        output.seek(0)
        
        return Response(output.read(), status=self.status)


    def boundingbox_crop(self, request, format=None, id=None):
        '''
        endpoint for displaying and downloading the boundingbox-crop in original size
        '''
        output = BytesIO()
        img = self.get_boundingbox_crop(id)
        img = self.resize(request, img)
        img.save(output, format=self.ext)
        output.seek(0)
        
        return Response(output.read(), status=self.status)


    def segmentation_crop(self, request, format=None, id=None):
        '''
        endpoint for displaying and downloading the segmentation as an image in original size
        '''
        output = BytesIO()
        img = self.get_segmentation_crop(id)
        img = self.resize(request, img)
        img.save(output, format=self.ext)
        output.seek(0)
        
        return Response(output.read(), status=self.status)


    def plot(self, request, format=None):
        '''
        endpoint for plot preview of seleted types of images
        '''
        output = BytesIO()
        if 'ids' not in request.query_params:
            return HttpResponse('false')

        image_type = request.query_params.get('type', 'all')
        ids = request.query_params.get('ids').split(',')

        height = 200
        width = 200
        padding = 30
        background_color = (255,255,255,0)

        imgs = []
        for uid in ids:
            if image_type == 'boundingbox':
                type_id = uid.split('-')[-1]
                img = self.get_boundingbox_crop(type_id)
            elif image_type == 'segmentation':
                type_id = uid.split('-')[-1]
                background_color = (0,0,0,0)
                img = self.get_segmentation_crop(type_id)
            else:
                image_id = uid.split('-')[0]
                img = self.get_image(image_id)
            
            if img:
                img.thumbnail((width,height), PImage.ANTIALIAS)
                imgs.append(img)

        widths, heights = zip(*(i.size for i in imgs))

        
        total_width = sum(widths) + (len(widths)-1)*padding

        new_im = PImage.new('RGB', (total_width, height), color=background_color)

        x_offset = 0
        for img in imgs:
            y_offset = math.floor((height - img.height)/2)
            new_im.paste(img, (x_offset,y_offset))
            x_offset += img.size[0] + padding

        new_im.save(output, format=self.ext)
        output.seek(0)
        return Response(output.read(), status=self.status)


    def find_and_open_image(self, image_id):
        '''
        return pil image object and open image object by image_id
        '''
        self.status = 404
        try:
            image = Image.objects.get(id=image_id)
        except:
            image = False
            

        if image and image.path is not None and len(image.path) > 0:
            if os.path.exists(os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path)):
                img_path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path)
                self.status = 200
            img = PImage.open(img_path).convert('RGB')
        
        elif image and image.url is not None:
            response = requests.get(image.url)
            if response.status_code is 200:
                img = PImage.open(BytesIO(response.content))
                self.status = 200
        else:
            img_path = 'images/data/empty.png'
            img = PImage.open(img_path).convert('RGB')

        return (image, img)


    def get_image(self, image_id):
        '''
        return pil image object by image_id
        '''       
        image = Image.objects.get(id=image_id)
        img = PImage.open(os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path))
        return img


    def get_annotation(self, annotation_id):
        '''
        return pil image object by annotation_id
        '''
        an = Annotation.objects.get(id=annotation_id)
        (image, img) = self.find_and_open_image(an.image.id)
        return img


    def get_boundingbox_crop(self, annotation_boundingbox_id):
        '''
        return pil image object by annotation_boundingbox_id
        '''
        bb = AnnotationBoundingbox.objects.get(id=annotation_boundingbox_id)
        img = PImage.open(os.path.join(settings.DATAFRONTEND['DATA_PATH'], bb.image.path))
        img = img.crop((bb.x_min*img.width, bb.y_min*img.height, bb.x_max*img.width, bb.y_max*img.height))
        return img


    def get_segmentation_crop(self, annotation_segmentation_id):
        '''
        return pil image object by annotation_segmentation_id
        '''
        sg = AnnotationSegmentation.objects.get(id=annotation_segmentation_id)

        if sg.segmentation:
            mask = np.zeros([[sg.image.height, sg.image.width], count], dtype=np.uint8) # wrong order?
            for i, landmarks in enumerate(sg.segmentation):
                img = Image.new('L', (sg.image.width, sg.image.height), 0)
                for landmark in landmarks:
                    ImageDraw.Draw(img).polygon(landmark, outline=0, fill=1)
                mask[:, :, i] = np.array(img)
        elif sg.mask:
            rle_struct = [
                {
                    'counts': sg.mask,
                    'size': [ sg.height, sg.width ]
                }
            ]
            
            decoded_mask = mask.decode(rle_struct)
        mask = np.squeeze(decoded_mask)

        mask_image = PImage.fromarray(mask)
        mat = np.reshape(mask_image,(sg.height, sg.width))

        overlay = PImage.fromarray(np.uint8(mat * 255) , 'L')

        return overlay


    def draw_boundingbox(self, image, img):
        '''
        draw boundingboxes from image on img image-canvas
        '''

        bounding_boxes = image.annotationboundingbox_set.all()

        for bbox in bounding_boxes:
            draw = ImageDraw.Draw(img)
            draw.rectangle(((bbox.x_min*img.width, bbox.y_min*img.height), (bbox.x_max*img.width, bbox.y_max*img.height)), fill=None, outline='red', width=5)

        return img

    
    def svg_segmentation(self, request, format=None, id=None):
        '''
        draw segmentation from image
        '''
        (image, img) = self.find_and_open_image(id)
        segmentations = image.annotationsegmentation_set.all()
        
        layers = []
        for segmentation in segmentations:
            layer = []
            if segmentation.segmentation:
                first_point = []
                for il, landmarks in enumerate(segmentation.segmentation):
                    if type(landmarks) is not list:
                        continue
                    for ip, point in enumerate(np.array_split(landmarks, (len(landmarks)/2))):
                        if ip is 0:
                            layer.append('M %s %s' % (point[0], point[1]))
                            first_point = 'L %s %s' % (point[0], point[1])
                        else:
                            layer.append('L %s %s' % (point[0], point[1]))
                    # close figure with goto start
                    if len(landmarks) > 2:
                        layer.append(first_point)
                #layer.append('z')
                layers.append('''<g class="segmentation_layer" style="">
                        <title>%s</title>
                        <path
                            class="segmentation_path"
                            fill="transparent"
                            stroke="#ff0000"
                            stroke-opacity="1"
                            stroke-width="2"
                            stroke-dasharray="none"
                            stroke-linejoin="round"
                            stroke-linecap="butt"
                            stroke-dashoffset=""
                            fill-rule="nonzero"
                            opacity="1"
                            marker-start=""
                            marker-mid=""
                            marker-end=""
                            id="seg_%s"
                            d="%s"
                            style="color: rgb(0, 0, 0);"/>
                    </g>
                    ''' % (
                        segmentation.category.name,
                        segmentation.id,
                        (' '.join(layer))
                    )
                )    


        # Reference: https://developer.mozilla.org/de/docs/Web/SVG/Tutorial/Pfade
        data = '''
            <svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" style="">
                <title>%s</title>
                <rect id="backgroundrect" width="%s" height="%s" x="0" y="0" fill="transparent" stroke="none"/>
                %s
            </svg>
        ''' % (image.width, image.height, image.name, '100%', '100%', ' '.join(layers))

        return HttpResponse(data, status=200, content_type="image/svg+xml");


    def draw_segmentation(self, image, img):
        '''
        draw segmentation from image
        '''
        segmentations = image.annotationsegmentation_set.all()
        
        if len(segmentations) == 0:
            return img

        img = False
        for segmentation in segmentations:
            if segmentation.segmentation:
                #info = self.image_info[image_id]
                count = len(segmentation.segmentation)
                mask = np.zeros([segmentation.image.height, segmentation.image.width], dtype=np.uint8) # wrong order?
                #print(segmentation.segmentation)
                imgg = PImage.new('L', (segmentation.image.width, segmentation.image.height), 0)
                for i, landmarks in enumerate(segmentation.segmentation):
                    #imgg = PImage.new('L', (segmentation.image.width, segmentation.image.height), 0)
                    #for landmark in landmarks:
                    #print(landmarks)
                    ImageDraw.Draw(imgg).polygon(landmarks, outline=10, fill=0)
                #mask[:, :] = np.array(imgg)

                #class_ids = np.array(info['class_ids'])
                # return mask, class_ids.astype(np.int32)
                # return None
                #mask_image = PImage.fromarray(mask)
                mat = np.reshape(imgg,(segmentation.image.height, segmentation.image.width))
            elif segmentation.mask:
                width
                rle_struct = [
                    {
                        'counts': segmentation.mask,
                        'size': [ segmentation.height, segmentation.width ]
                    }
                ]
                
                decoded_mask = mask.decode(rle_struct)
                mask = np.squeeze(decoded_mask)

                mask_image = PImage.fromarray(mask)
                mat = np.reshape(mask_image,(segmentation.height, segmentation.width))

            overlay = PImage.fromarray(np.uint8(mat * 255) , 'L')

            if img:
                img = PImage.blend(img, overlay, alpha=0.8)
            else:
                img = overlay
            
        return img

