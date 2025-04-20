from django.contrib.auth import get_user_model
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


class AdminNodeTests(TestCase):
    """Тесты для административного интерфейса модели Node."""

    def setUp(self):
        """Создание тестового пользователя и тестовых объектов."""
        self.user = get_user_model().objects.create_superuser(
            username='admin',
            password='password'
        )
        self.node1 = Node.objects.create(name='Node 1', city='City A', supplier='Supplier A', debt=100)
        self.node2 = Node.objects.create(name='Node 2', city='City A', supplier='Supplier B', debt=200)

    def test_list_display(self):
        """Проверка правильного отображения списка объектов Node."""
        self.client.login(username='admin', password='password')
        response = self.client.get('/admin/app_name/node/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.node1.name)
        self.assertContains(response, self.node2.name)
        self.assertContains(response, self.node1.debt)
        self.assertContains(response, self.node2.debt)

    def test_clear_debt_action(self):
        """Проверка выполнения действия очистки задолженности."""
        self.client.login(username='admin', password='password')

        # Убедимся, что у узлов есть задолженность перед выполнением действия
        self.assertEqual(self.node1.debt, 100)
        self.assertEqual(self.node2.debt, 200)

        response = self.client.post(
            '/admin/app_name/node/action/',
            {'post': 'clear_debt', '_selected_action': [self.node1.id, self.node2.id]}
        )

        # Проверка, что задолженность очищена
        self.node1.refresh_from_db()
        self.node2.refresh_from_db()
        self.assertEqual(self.node1.debt, 0)
        self.assertEqual(self.node2.debt, 0)
        self.assertContains(response, "Задолженность успешно очищена")


class AdminProductTests(TestCase):
    """Тесты для административного интерфейса модели Product."""

    def setUp(self):
        """Создание тестового пользователя и тестовых объектов."""
        self.user = get_user_model().objects.create_superuser(
            username='admin',
            password='password'
        )
        self.node = Node.objects.create(name='Node 1', city='City A', supplier='Supplier A', debt=100)
        self.product = Product.objects.create(name='Product 1', model='Model 1', release_date='2023-01-01',
                                              node=self.node)

    def test_product_list_display(self):
        """Проверка правильного отображения списка объектов Product."""
        self.client.login(username='admin', password='password')
        response = self.client.get('/admin/app_name/product/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.model)
        self.assertContains(response, self.product.release_date)
        self.assertContains(response, self.product.node.name)
