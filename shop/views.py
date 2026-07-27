from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def product_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'categories': categories})

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