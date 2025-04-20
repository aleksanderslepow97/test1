from rest_framework import serializers
from .models import Node, Product


class NodeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели узла (Node).

    Этот сериализатор используется для преобразования
    экземпляров модели узла в JSON и обратно, что позволяет
    легко взаимодействовать с данными узла через API.

    Метаданные:
        model (Model): Модель, с которой связан этот сериализатор (Node).
        fields (list): Все поля модели, которые будут включены
        в сериализацию и десериализацию.
    """

    class Meta:
        model = Node
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели продукта (Product).

    Этот сериализатор используется для преобразования
    экземпляров модели продукта в JSON и обратно, что позволяет
    легко взаимодействовать с данными продукта через API.

    Метаданные:
        model (Model): Модель, с которой связан этот сериализатор (Product).
        fields (list): Все поля модели, которые будут включены
        в сериализацию и десериализацию.
    """

    class Meta:
        model = Product
        fields = '__all__'
