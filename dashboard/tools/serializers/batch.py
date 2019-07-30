from rest_framework import serializers
from tools.models import Batch


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = ( 'id', 'action', 'params', 'log', 'status', 'created_at', 'updated_at' )
