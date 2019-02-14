from rest_framework import generics
from rest_framework import viewsets

from rest_framework import filters

from .serializers import *
from .models import *


class EnumTypeViewset(viewsets.ModelViewSet):

    queryset = EnumType.objects.all()
    serializer_class = EnumTypeSerializer


class EnumViewset(viewsets.ModelViewSet):

    queryset = Enum.objects.all()
    serializer_class = EnumSerializer
    # filter_backends = (filters.SearchFilter,)
    filter_fields = ('enumtype_id',)
    # search_fields = ('enumtype__ref',)
