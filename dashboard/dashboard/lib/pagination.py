import json

from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response

# reference here:
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
class Pagination(pagination.LimitOffsetPagination):
    
    start = False
    stop = False


    def decode_request(self, key, request):
        params_str = request.query_params.get(key)
        if params_str is not None and params_str is not '':
            return json.loads(params_str.replace("\'", "\""))
        return {}


    def set_range(self, request):
        if self.start:
            return

        self.start = 0
        self.stop = settings.REST_FRAMEWORK['PAGE_SIZE'] - 1

        filter_params = self.decode_request('filter', request)
        range_params = self.decode_request('range', request)
        if 'max' in filter_params:
            self.stop = int(filter_params['max']) - 1
        elif len(range_params) == 2:
            self.start, self.stop = range_params


    def get_limit(self, request):
        self.set_range(request)
        return self.stop - self.start + 1


    def get_offset(self, request):
        self.set_range(request)
        
        return self.start


    def get_paginated_response(self, data):

        return Response(data, headers={
            'Content-Range': ('%s-%s/%s') % (self.start, self.stop, self.count),
        })
