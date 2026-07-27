from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .cart import get_cart, add_to_cart, remove_from_cart
from .forms import OrderForm
from django.contrib import messages

def product_list(request):
    categories = Category.objects.all()
    cart = get_cart(request)
    cart_count = cart.items.count()
    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'cart_count': cart_count,
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(in_stock=True)
    cart = get_cart(request)
    cart_count = cart.items.count()
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
        'cart_count': cart_count,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = get_cart(request)
    cart_count = cart.items.count()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_count': cart_count,
    })

def add_to_cart_view(request, slug):
    add_to_cart(request, slug)
    return redirect('product_detail', slug=slug)

def cart_view(request):
    cart = get_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def remove_from_cart_view(request, item_id):
    from .models import CartItem
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart_view')

def update_cart_view(request, item_id, action):
    from .models import CartItem
    cart_item = CartItem.objects.get(id=item_id)
    
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            cart_item.delete()
            return redirect('cart_view')
    
    cart_item.save()
    return redirect('cart_view')

def checkout_view(request):
    cart = get_cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = cart.total_price()
            order.save()
            
            # Сохраняем товары из корзины в заказ
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            
            messages.success(request, f'Заказ #{order.id} успешно оформлен!')
            return redirect('product_list')
    else:
        form = OrderForm()
    
    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart': cart,
    })

def search_view(request):
    query = request.GET.get('q', '')
    products = []
    
    if query:
        query_lower = query.lower()
        all_products = Product.objects.filter(in_stock=True)
        
        for product in all_products:
            if query_lower in product.name.lower() or query_lower in product.category.name.lower():
                products.append(product)
    
    cart = get_cart(request)
    cart_count = cart.items.count()
    
    return render(request, 'shop/search_results.html', {
        'query': query,
        'products': products,
        'cart_count': cart_count,
    })

def cart_count(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
        return {'cart_count': cart.items.count()}
    return {'cart_count': 0}