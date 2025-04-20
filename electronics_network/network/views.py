# from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Node
from .serializers import NodeSerializer


class NodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели узла (Node).

    Этот ViewSet предоставляет полный набор представлений для
    модели Node, включая создание, чтение, обновление и удаление
    узлов. В методе обновления запрещено изменение поля 'debt',
    если оно присутствует в запросе.

    Атрибуты:
        queryset: Все экземпляры модели Node.
        serializer_class: Сериализатор, используемый для обработки
                          экземпляров Node.

    Методы:
        update: Переопределяет стандартный метод обновления, чтобы
                исключить обновление поля 'debt'.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def update(self, request, *args, **kwargs):
        """
        Переопределенный метод обновления.

        Запрещает обновление поля 'debt' в запросе,
        если оно присутствует в данных запроса.
        Удаляет 'debt' из данных запроса перед вызовом
        стандартного метода обновления.

        Аргументы:
            request: Объект запроса, содержащий данные для обновления.
            *args: Дополнительные аргументы.
            **kwargs: Ключевые аргументы.

        Возвращает:
            Response: Ответ API после обработки запроса обновления.
        """
        instance = self.get_object()
        debt = request.data.get('debt', None)
        if debt is not None:
            request.data.pop('debt')
        return super().update(request, *args, **kwargs)


class NobeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели узла (Node) с ограничениями доступа.

    Этот ViewSet предоставляет полный набор представлений для
    модели Node и требует аутентификации для выполнения действий.
    Включает возможность фильтрации узлов по стране.

    Атрибуты:
        queryset: Все экземпляры модели Node.
        serializer_class: Сериализатор, используемый для обработки
                          экземпляров Node.
        permission_classes: Список классов разрешений для контроля доступа.

    Методы:
        get_queryset: Переопределяет метод получения запроса для
                      фильтрации узлов по стране.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Переопределенный метод получения запроса.

        Фильтрует queryset узлов по стране, если параметр 'country'
        указан в запросе. Возвращает отфильтрованный queryset.

        Возвращает:
            QuerySet: Отфильтрованный набор объектов Node.
        """
        queryset = super().get_queryset()
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country=country)
        return queryset
