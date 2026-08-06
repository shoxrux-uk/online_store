from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem, Order, OrderItem, PromoCode, Color
from .cart import get_cart, add_to_cart, remove_from_cart
from .forms import OrderForm

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)
    hits = Product.objects.filter(in_stock=True)[:3]
    new = Product.objects.filter(in_stock=True).order_by('-created_at')[:3]
    
    cart = get_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    
    context = {
        'categories': categories,
        'products': products,
        'hits': hits,
        'new': new,
        'cart_count': total_items,
    }
    
    return render(request, 'shop/product_list.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(in_stock=True)
    cart = get_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
        'cart_count': total_items,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = get_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_count': total_items,
    })

@login_required
def add_to_cart_view(request, slug):
    add_to_cart(request, slug)
    return redirect('product_detail', slug=slug)

@login_required
def cart_view(request):
    cart = get_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

@login_required
def remove_from_cart_view(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def update_cart_view(request, item_id, action):
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

@login_required
def checkout_view(request):
    cart = get_cart(request)
    discount = 0
    promo_code = None
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            promo_code_input = request.POST.get('promo_code')
            if promo_code_input:
                try:
                    promo = PromoCode.objects.get(
                        code__iexact=promo_code_input,
                        is_active=True,
                        valid_until__gte=timezone.now()
                    )
                    discount = promo.discount
                    promo_code = promo
                except PromoCode.DoesNotExist:
                    messages.warning(request, 'Промокод недействителен или истёк')
            
            total = cart.total_price()
            discount_amount = total * discount / 100
            final_total = total - discount_amount
            
            order = form.save(commit=False)
            order.total_price = final_total
            order.user = request.user
            order.status = 'pending'  # ← статус по умолчанию
            order.save()
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    color=item.color,
                    size=item.size
                )
            
            cart.items.all().delete()
            
            messages.success(request, f'Заказ #{order.id} успешно оформлен!')
            if promo_code:
                messages.info(request, f'Применена скидка {discount}% по промокоду {promo_code.code}')
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
    total_items = sum(item.quantity for item in cart.items.all())
    
    return render(request, 'shop/search_results.html', {
        'query': query,
        'products': products,
        'cart_count': total_items,
    })

def check_promo(request):
    code = request.GET.get('code', '')
    total = float(request.GET.get('total', 0))
    
    if code:
        try:
            promo = PromoCode.objects.get(
                code__iexact=code,
                is_active=True,
                valid_until__gte=timezone.now()
            )
            discount = float(promo.discount)
            discount_amount = total * discount / 100
            new_total = total - discount_amount
            
            return JsonResponse({
                'valid': True,
                'discount': discount,
                'discount_amount': round(discount_amount, 2),
                'new_total': round(new_total, 2),
                'message': f'✅ Промокод активирован! Скидка {discount}%'
            })
        except PromoCode.DoesNotExist:
            return JsonResponse({
                'valid': False,
                'message': '❌ Промокод недействителен или истёк'
            })
    
    return JsonResponse({
        'valid': False,
        'message': '❌ Введите промокод'
    })

def cart_count(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
        total_items = sum(item.quantity for item in cart.items.all())
        return {'cart_count': total_items}
    return {'cart_count': 0}