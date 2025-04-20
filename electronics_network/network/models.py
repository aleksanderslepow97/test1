# from django.db import models

# Create your models here.
from django.db import models


class Node(models.Model):
    """Модель, представляющая узел (поставщика) в системе.

    Узел может быть заводом, розничной сетью или индивидуальным предпринимателем.

    Атрибуты:
        name (CharField): Название узла.
        email (EmailField): Электронная почта узла.
        country (CharField): Страна расположения узла.
        city (CharField): Город расположения узла.
        street (CharField): Улица расположения узла.
        house_number (CharField): Номер дома.
        supplier (ForeignKey): Ссылка на другого узла, если этот узел является поставщиком (возможно, null).
        debt (DecimalField): Текущая задолженность узла, выраженная в десятичном формате.
        created_at (DateTimeField): Дата и время создания записи о узле.
        level (IntegerField): Уровень узла, определяющий его тип (завод, розничная сеть, ИП).
    """

    objects = None
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель')
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='suppliers')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(choices=LEVEL_CHOICES)

    def __str__(self):
        """Возвращает название узла как строковое представление."""
        return self.name


class Product(models.Model):
    """Модель, представляющая продукт, связанный с узлом.

    Продукт может быть ассоциирован с конкретным узлом (поставщиком), что позволяет
    связать продукты с их источниками.

    Атрибуты:
        name (CharField): Название продукта.
        model (CharField): Модель продукта.
        release_date (DateField): Дата выпуска продукта.
        node (ForeignKey): Ссылка на узел (поставщика), к которому принадлежит продукт.
    """

    objects = None
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    node = models.ForeignKey(Node, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает название продукта как строковое представление."""
        return self.name
