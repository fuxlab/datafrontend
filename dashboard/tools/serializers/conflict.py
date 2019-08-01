from rest_framework import serializers
from tools.models import Conflict


class ConflictSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conflict
        fields = ( 'id', 'status', 'reason', 'affected_ids', 'message', 'created_at', 'updated_at' )
