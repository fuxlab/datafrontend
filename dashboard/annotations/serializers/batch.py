from rest_framework import serializers
from annotations.models import Batch


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = ( 'id', 'action', 'params', 'log' )