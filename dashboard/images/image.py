from rest_framework import permissions
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
import os
from io import BytesIO

from PIL import Image as PImage
from PIL import ImageDraw
import pycocotools.mask as mask
import numpy as np

from images.models import Image


class PNGRenderer(renderers.BaseRenderer):
    
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, image_data, media_type=None, renderer_context=None):
        return image_data


class ImagePreview(APIView):
    
    permission_classes = [
        permissions.AllowAny
    ]

    renderer_classes = (PNGRenderer, )

    def get(self, request, format=None, image_id=None):
        try:
            image = Image.objects.get(id=image_id)
        except:
            image = False
        
        if image and image.path is not None and len(image.path) > 0:
            img_path = os.path.join(settings.DATAFRONTEND['DATA_PATH'], image.path)
        else:
            img_path = 'images/data/empty.png'
        
        output = BytesIO()
        im = PImage.open(img_path)
        
        image_type = self.request.query_params.get('type')
        if image_type is not None:
            if image_type == 'boundingbox':
                im = self.draw_boundingbox(image, im)
            if image_type == 'segmentation':
                im = self.draw_segmentation(image, im)
            im.thumbnail((800,600))
        else:
            im.thumbnail((200,200))
        
        im.save(output, format='PNG')
        output.seek(0)
        
        return Response(output.read())


    def draw_boundingbox(self, image, im):
        bounding_boxes = image.annotationboundingbox_set.all()

        for bbox in bounding_boxes:
            draw = ImageDraw.Draw(im)
            draw.rectangle(((bbox.x_min*im.width, bbox.y_min*im.height), (bbox.x_max*im.width, bbox.y_max*im.height)), fill=None, outline='red', width=5)

        return im


    def draw_segmentation(self, image, im):
        segmentations = image.annotationsegmentation_set.all()
        
        if len(segmentations) == 0:
            return im

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