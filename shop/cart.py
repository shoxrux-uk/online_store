from .models import Cart, CartItem, Product, Color

def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request, product_slug, color_id=None):
    product = Product.objects.get(slug=product_slug)
    cart = get_cart(request)
    
    color = None
    if color_id:
        try:
            color = Color.objects.get(id=color_id)
        except Color.DoesNotExist:
            pass
    
    # Если цвет не выбран, но у товара есть цвета — сохраняем первый доступный
    if not color and product.colors.exists():
        color = product.colors.first()
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        color=color,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()