from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<catname>', views.products, name='category'),
    path('product/<prodslug>', views.productdetails, name='product'),
    path('search', views.search, name='search'),
    path('cart', views.cart, name='cart'),
    path('addtocart/<product_id>/<quantity>', views.addtocart, name='addtocart'),
    path('removeproduct/<pid>', views.removeproduct, name='removeproduct'),
    path('quantity/<op>/<pid>', views.quantity, name='quantity'),
    path('success', views.success, name='success'),
    path('shop/', views.shop, name='shop'),
    path('pp/', views.pp, name='pp'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
