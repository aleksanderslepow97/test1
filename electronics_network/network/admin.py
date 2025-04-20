# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Node, Product


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Node.

    Позволяет управлять объектами Node в административной панели Django.

    Атрибуты:
        list_display (tuple): Кортеж атрибутов, которые отображаются в списке объектов Node.
        list_filter (tuple): Кортеж атрибутов, по которым можно фильтровать объекты Node.
        actions (list): Список доступных действий, которые можно выполнять над выбранными объектами Node.
    """

    list_display = ('name', 'city', 'supplier', 'debt', 'created_at')
    list_filter = ('city',)
    actions = ['clear_debt']

    def clear_debt(self, request, queryset):
        """Очистить задолженность для выбранных объектов Node.

        Обновляет поле `debt` выбранных объектов до 0 и отображает сообщение об успешном выполнении.

        Аргументы:
            request (HttpRequest): Объект запроса от текущего пользователя.
            queryset (QuerySet): Набор выбранных объектов Node, для которых будет выполнено действие.
        """
        queryset.update(debt=0)
        self.message_user(request, "Задолженность успешно очищена")

    clear_debt.short_description = "Очистить задолженность для выбранных объектов"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели Product.

    Позволяет управлять объектами Product в административной панели Django.

    Атрибуты:
        list_display (tuple): Кортеж атрибутов, которые отображаются в списке объектов Product.
    """

    list_display = ('name', 'model', 'release_date', 'node')
