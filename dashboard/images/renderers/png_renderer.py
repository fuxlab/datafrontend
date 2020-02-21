from rest_framework import permissions, renderers, viewsets

class PNGRenderer(renderers.BaseRenderer):
    
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, image_data, media_type=None, renderer_context=None):
        return image_data
