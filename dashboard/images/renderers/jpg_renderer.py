from rest_framework import permissions, renderers, viewsets

class JPGRenderer(renderers.BaseRenderer):
    
    media_type = 'image/jpeg'
    format = 'jpeg'
    charset = None
    render_style = 'binary'

    def render(self, image_data, media_type=None, renderer_context=None):
        return image_data

