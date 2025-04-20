# from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Node
from .serializers import NodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Запрет на обновление задолженности
        debt = request.data.get('debt', None)
        if debt is not None:
            request.data.pop('debt')
        return super().update(request, *args, **kwargs)


class NobeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Пример фильтрации по стране
        queryset = super().get_queryset()
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country=country)
        return queryset
