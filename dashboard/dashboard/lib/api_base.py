import json

from rest_framework.views import APIView
from rest_framework import viewsets

class ApiBase(APIView):

    def get_filter(self):
        '''
        return filter params
        '''
        filter_params_str = self.request.query_params.get('filter')
        if filter_params_str is not None:
            return json.loads(filter_params_str.replace("\'", "\""))
        
        return []


    def get_sort(self):
        '''
        db sorting of  results
        '''
        sort_field = 'id'
        sort_order = 'ASC'

        sort_params_str = self.request.query_params.get('sort')
        if sort_params_str is not None:
            sort_field, sort_order = json.loads(sort_params_str.replace("\'", "\""))

        if sort_order == 'DESC':
            sort_order = '-'
        else:
            sort_order = ''
        
        return '%s%s' % (sort_order, sort_field)

    
    def apply_range(self, queryset):
        '''
        depricated:
        apply range params to queryset if requested
        '''
        default_size = 10

        range_params_str = self.request.query_params.get('range')
        if range_params_str is not None:
            start, stop = json.loads(range_params_str.replace("\'", "\""))
            count = stop - start
            return queryset[start:stop]
        
        return queryset



class DashboardApiBase(viewsets.ModelViewSet):

    def get_filter(self):
        return ApiBase.get_filter(self)

    def get_sort(self):
        return ApiBase.get_sort(self)

    def apply_range(self, queryset):
        return ApiBase.apply_range(self, queryset)