from rest_framework import permissions
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

from images.models import Image
from PIL import Image as PImage
from io import BytesIO
import base64, os


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
        im.thumbnail((200,200))
        im.save(output, format='PNG')
        output.seek(0)
        output_s = output.read()
        b64 = base64.b64encode(output_s)

        return Response(output_s)