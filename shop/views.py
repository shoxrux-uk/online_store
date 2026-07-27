from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from .cart import get_cart 

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
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

from .cart import get_cart, add_to_cart, remove_from_cart

def cart_view(request):
    cart = get_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})

def add_to_cart_view(request, slug):
    add_to_cart(request, slug)
    return redirect('product_detail', slug=slug)

from .cart import get_cart

def cart_count(request):
    if request.user.is_authenticated:
        cart = get_cart(request)
        return {'cart_count': cart.items.count()}
    return {'cart_count': 0}