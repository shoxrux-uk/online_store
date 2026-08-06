from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Изображение')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Иконка (эмодзи)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название цвета')
    code = models.CharField(max_length=20, verbose_name='HEX-код', help_text='Например: #000000')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name='Размер')
    category_type = models.CharField(
        max_length=20,
        choices=[
            ('clothing', 'Одежда'),
            ('shoes', 'Обувь'),
            ('furniture', 'Мебель'),
            ('universal', 'Универсальный'),
        ],
        default='universal',
        verbose_name='Тип категории'
    )
    sort_order = models.IntegerField(default=0, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['sort_order']


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    colors = models.ManyToManyField(Color, blank=True, verbose_name='Доступные цвета')
    sizes = models.ManyToManyField(Size, blank=True, verbose_name='Доступные размеры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name='Товар')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    is_main = models.BooleanField(default=False, verbose_name='Основное фото')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"Фото для {self.product.name}"

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class Cart(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.session_key}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цвет')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Размер')

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        color_name = f" ({self.color.name})" if self.color else ""
        size_name = f" ({self.size.name})" if self.size else ""
        return f"{self.product.name}{color_name}{size_name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '⏳ В обработке'),
        ('confirmed', '✅ Подтверждён'),
        ('shipped', '🚚 Отправлен'),
        ('delivered', '📦 Доставлен'),
        ('cancelled', '❌ Отменён'),
    ]

    PAYMENT_CHOICES = [
        ('card', '💳 Картой онлайн'),
        ('cash', '📦 При получении'),
        ('installment', '📱 Рассрочка'),
    ]

    INSTALLMENT_CHOICES = [
        (3, '3 месяца'),
        (6, '6 месяцев'),
        (12, '12 месяцев'),
        (24, '24 месяца'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    address = models.TextField(verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash',
        verbose_name='Способ оплаты'
    )
    
    card_number = models.CharField(max_length=19, blank=True, null=True, verbose_name='Номер карты')
    card_expiry = models.CharField(max_length=5, blank=True, null=True, verbose_name='Срок (MM/YY)')
    
    installment_months = models.IntegerField(
        choices=INSTALLMENT_CHOICES,
        blank=True,
        null=True,
        verbose_name='Срок рассрочки (месяцев)'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус заказа'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Итого')

    def __str__(self):
        return f"Заказ #{self.id} - {self.full_name}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цвет')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Размер')

    def __str__(self):
        color_name = f" ({self.color.name})" if self.color else ""
        size_name = f" ({self.size.name})" if self.size else ""
        return f"{self.product.name}{color_name}{size_name} x {self.quantity}"

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Промокод')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка (%)')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    valid_until = models.DateTimeField(verbose_name='Действителен до')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.code} - {self.discount}%"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'