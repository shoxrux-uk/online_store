from django import template

register = template.Library()

@register.filter
def sum_format(value):
    """
    Форматирует число как узбекские сумы
    Пример: 1000 -> 1 000 so'm
             1000000 -> 1 000 000 so'm
    """
    try:
        # Преобразуем в целое число (если это Decimal или float)
        value = int(float(value))
        # Форматируем с пробелами между разрядами
        formatted = f"{value:,}".replace(',', ' ')
        return f"{formatted} so'm"
    except (ValueError, TypeError):
        return f"{value} so'm"