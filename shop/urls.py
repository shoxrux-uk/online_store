from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart_view, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('search/', views.search_view, name='search'),
    path('check-promo/', views.check_promo, name='check_promo'),
]