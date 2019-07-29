from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets

from django.http import HttpResponse
from rest_framework.response import Response

from django.conf import settings
import os, math
from io import BytesIO

from PIL import Image as PImage
from PIL import ImageDraw
import pycocotools.mask as mask
import numpy as np

from images.models import Image
from annotations.models import Annotation, AnnotationBoundingbox, AnnotationSegmentation


class PNGRenderer(renderers.BaseRenderer):
    
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, image_data, media_type=None, renderer_context=None):
        return image_data


class ImageRenderer(viewsets.ModelViewSet):
    
    permission_classes = [
        permissions.AllowAny
    ]

    renderer_classes = (PNGRenderer, )



    def thumbnail(self, request, format=None, id=None):
        (image, img) = ImageRenderer.find_and_open_image(id)
        output = BytesIO()
        img.thumbnail((200,200))
        img.save(output, format='PNG')
        output.seek(0)
        
        return Response(output.read())


    def preview(self, request, format=None, id=None):
        '''
        endpoint for image preview with maximum 800x600 size
        optional with boundingboxes, and segmentation overlay
        '''
        (image, img) = ImageRenderer.find_and_open_image(id)
        output = BytesIO()
        
        image_type = self.request.query_params.get('type')
        if image_type is not None:
            if image_type == 'boundingbox':
                img = ImageRenderer.draw_boundingbox(image, img)
            if image_type == 'segmentation':
                img = ImageRenderer.draw_segmentation(image, img)
        
        img.thumbnail((800,600))
        img.save(output, format='PNG')
        output.seek(0)
        return Response(output.read())


    def original(self, request, format=None, id=None):
        '''
        endpoint to render original image
        '''
        (image, img) = ImageRenderer.find_and_open_image(id)

        output = BytesIO()
        img.save(output, format='PNG')
        output.seek(0)
        
        return Response(output.read())


    def find_and_open_image(image_id):
        '''
        return pil image object and open image object by image_id
        '''
        try:
            image = Image.objects.get(id=image_id)
        except:
            image = False

        img_path = 'images/data/empty.png'
        if image and image.path is not None and len(image.path) > 0:
            if os.path.exists(img_path):
                img_path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path)
        
        img = PImage.open(os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path))
        return (image, img)


    def get_image(image_id):
        '''
        return pil image object by image_id
        '''       
        image = Image.objects.get(id=image_id)
        img = PImage.open(os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path))
        return img


    def get_annotation(annotation_id):
        '''
        return pil image object by annotation_id
        '''
        an = Annotation.objects.get(id=annotation_id)
        (image, img) = ImageRenderer.find_and_open_image(an.image.id)
        return img


    def get_boundingbox_crop(annotation_boundingbox_id):
        '''
        return pil image object by annotation_boundingbox_id
        '''
        bb = AnnotationBoundingbox.objects.get(id=annotation_boundingbox_id)
        img = PImage.open(os.path.join(settings.DATAFRONTEND['DATA_PATH'], bb.image.path))
        img = img.crop((bb.x_min*img.width, bb.y_min*img.height, bb.x_max*img.width, bb.y_max*img.height))
        return img


    def get_segmentation_crop(annotation_segmentation_id):
        '''
        return pil image object by annotation_segmentation_id
        '''
        sg = AnnotationSegmentation.objects.get(id=annotation_segmentation_id)


        rle_struct = [
            {
                'counts': sg.mask,
                'size': [ sg.height, sg.width ]
            }
        ]
        
        decoded_mask = mask.decode(rle_struct)
        numpy_mask = np.squeeze(decoded_mask)

        mask_image = PImage.fromarray(numpy_mask)
        mat = np.reshape(mask_image,(sg.height, sg.width))

        overlay = PImage.fromarray(np.uint8(mat * 255) , 'L')

        return overlay


    def boundingbox_crop(self, request, format=None, id=None):
        '''
        endpoint for displaying and downloading the boundingbox-crop in original size
        '''
        output = BytesIO()
        img = ImageRenderer.get_boundingbox_crop(id)
        img.save(output, format='PNG')
        output.seek(0)
        
        return Response(output.read())


    def segmentation_crop(self, request, format=None, id=None):
        '''
        endpoint for displaying and downloading the segmentation as an image in original size
        '''
        output = BytesIO()
        img = ImageRenderer.get_segmentation_crop(id)
        img.save(output, format='PNG')
        output.seek(0)
        
        return Response(output.read())


    def plot(self, request, format=None):
        '''
        plot preview of seleted types of images
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
                img = ImageRenderer.get_boundingbox_crop(type_id)
            elif image_type == 'segmentation':
                type_id = uid.split('-')[-1]
                background_color = (0,0,0,0)
                img = ImageRenderer.get_segmentation_crop(type_id)
            else:
                image_id = uid.split('-')[0]
                img = ImageRenderer.get_image(image_id)
            
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

        new_im.save(output, format='PNG')
        output.seek(0)
        return Response(output.read())


    def draw_boundingbox(image, img):
        '''
        draw boundingboxes from image on img image-canvas
        '''

        bounding_boxes = image.annotationboundingbox_set.all()

        for bbox in bounding_boxes:
            draw = ImageDraw.Draw(img)
            draw.rectangle(((bbox.x_min*img.width, bbox.y_min*img.height), (bbox.x_max*img.width, bbox.y_max*img.height)), fill=None, outline='red', width=5)

        return img


    def draw_segmentation(image, img):
        '''
        draw segmentation from image
        '''
        segmentations = image.annotationsegmentation_set.all()
        
        if len(segmentations) == 0:
            return img

        img = False
        for segmentation in segmentations:
            
            rle_struct = [
                {
                    'counts': segmentation.mask,
                    'size': [ segmentation.height, segmentation.width ]
                }
            ]
            
            decoded_mask = mask.decode(rle_struct)
            numpy_mask = np.squeeze(decoded_mask)

            mask_image = PImage.fromarray(numpy_mask)
            mat = np.reshape(mask_image,(segmentation.height, segmentation.width))

            overlay = PImage.fromarray(np.uint8(mat * 255) , 'L')

            if img:
                img = PImage.blend(img, overlay, alpha=0.8)
            else:
                img = overlay
            
        return img
