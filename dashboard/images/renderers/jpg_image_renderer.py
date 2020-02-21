from images.renderers import ImageRenderer, JPGRenderer

class JPGImageRenderer(ImageRenderer):
    renderer_classes = (JPGRenderer, )
    ext = 'JPEG'
