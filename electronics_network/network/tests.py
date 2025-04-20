# from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.utils import timezone

from .models import Node, Product


class NodeModelTest(TestCase):
    """Тестирование модели Node."""

    def setUp(self):
        """Создание экземпляра Node для использования в тестах."""
        self.node = Node.objects.create(
            name='Test Node',
            email='test@mail.com',
            country='Country',
            city='City',
            street='Street',
            house_number='123',
            debt=100.00,
            level=0  # "Завод"
        )

    def test_node_creation(self):
        """Проверка, что Node создается с корректными атрибутами."""
        self.assertEqual(self.node.name, 'Test Node')
        self.assertEqual(self.node.email, 'test@mail.com')
        self.assertEqual(self.node.country, 'Country')
        self.assertEqual(self.node.city, 'City')
        self.assertEqual(self.node.street, 'Street')
        self.assertEqual(self.node.house_number, '123')
        self.assertEqual(self.node.debt, 100.00)
        self.assertEqual(self.node.level, 0)

    def test_node_str_method(self):
        """Проверка метода __str__ модели Node."""
        self.assertEqual(str(self.node), 'Test Node')


class ProductModelTest(TestCase):
    """Тестирование модели Product."""

    def setUp(self):
        """Создание экземпляра Node и Product для использования в тестах."""
        self.node = Node.objects.create(
            name='Test Node',
            email='test@mail.com',
            country='Country',
            city='City',
            street='Street',
            house_number='123',
            debt=100.00,
            level=0
        )
        self.product = Product.objects.create(
            name='Test Product',
            model='Model X',
            release_date=timezone.now().date(),
            node=self.node
        )

    def test_product_creation(self):
        """Проверка, что Product создается с корректными атрибутами."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.model, 'Model X')
        self.assertIsInstance(self.product.release_date, timezone.datetime)  # Проверка типа даты
        self.assertEqual(self.product.node, self.node)

    def test_product_str_method(self):
        """Проверка метода __str__ модели Product."""
        self.assertEqual(str(self.product), 'Test Product')
