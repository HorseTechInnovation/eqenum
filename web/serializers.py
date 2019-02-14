from .models import *

from rest_framework import serializers





class EnumTypeSerializer(serializers.ModelSerializer):


    class Meta:
        model = EnumType
        fields = ('ref','name','parent')


class EnumSerializer(serializers.ModelSerializer):


    class Meta:
        model = Enum
        fields = ('enumtype_id','ref', 'name', 'ordering')
