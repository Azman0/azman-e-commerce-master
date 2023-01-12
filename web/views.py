from django.shortcuts import render, redirect
from .models import SpecialProducts, Products, Categories, Cart
import uuid
from django.db.models import F
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.


def check_required(request, fields):
    warning = False
    for field in fields:
        if not request.POST[field] or request.POST[field].isspace():
            warning = True
    return warning


def set_validate(request, field, sanitize):
    strings = ["\'", "\"", ";", ">", "<", "/", "(", ")", "{", "}"]
    try:
        if not request.POST[field] or request.POST[field].isspace():
            return None
    except:
        return None
    else:
        data = request.POST[field]
        if sanitize:
            for x in strings:
                data.replace(x, '')
        return data

# --------------------------------------------------------------------


def index(request):
    hot_offer = SpecialProducts.objects.select_related('product_id').filter(type='hot-offer').exclude(product_id__status='hidden')
    featured_product = SpecialProducts.objects.select_related('product_id').filter(type='featured-product').exclude(product_id__status='hidden')

    return render(request, 'index.html', {"hot_offer": hot_offer, "featured_product": featured_product})


def products(request, catname):
    prods = Products.objects.filter(category_id = Categories.objects.get(slug = catname)).exclude(status='hidden').order_by('-id')
    paginator = Paginator(prods, 40)
    page = request.GET.get('page')
    prods = paginator.get_page(page)
    return render(request, 'products.html', {"prods": prods, "catname": catname, "paginator": paginator})


def productdetails(request, prodslug):
    prod = Products.objects.filter(slug=prodslug).exclude(status='hidden')
    return render(request, 'productDetails.html', {"prod": prod})


def cart(request):
    try:
        cartx = Cart.objects.select_related('product_id').filter(cart_no=request.session['cart_no'])
        products_cost = 0
        for item in cartx:
            products_cost += item.cost

        if products_cost >= 1:
            delivery_fees = 20
        else:
            delivery_fees = 0
            messages.error(request, 'YOUR CART IN EMPTY!')
        
        total_cost = products_cost + delivery_fees
        
        return render(request, 'cart.html', {"cartx": cartx, "products_cost": products_cost, "delivery_fees": delivery_fees, "total_cost": total_cost})
    except:
        messages.error(request, 'YOUR CART IS EMPTY!')
    
    return render(request, 'cart.html')


def addtocart(request, product_id, quantity):

    try:
        request.session['cart_no']
    except:
        request.session['cart_no'] = uuid.uuid4().hex[:10]  
    
    prod_price = Products.objects.get(id=product_id)
    prod_price = prod_price.final_price

    C = Cart.objects.filter(cart_no=request.session['cart_no'], product_id=product_id).update(
            quantity = F('quantity') + int(quantity), cost=F('cost') + int(prod_price)
        )
    if not C:
        Cart.objects.create(cart_no=request.session['cart_no'], product_id=Products.objects.get(id=int(product_id)), quantity=int(quantity), cost=prod_price)

    return redirect('cart')


def removeproduct(request, pid):
    try:
        Cart.objects.filter(cart_no=request.session['cart_no'], product_id=pid).delete()
    except Exception as e:
        pass
    return redirect('cart')


def quantity(request, op, pid):
    prod_price = Products.objects.get(id=pid)
    prod_price = prod_price.final_price

    if op == 'plus':
        C = Cart.objects.filter(cart_no=request.session['cart_no'], product_id=pid).update(
            quantity = F('quantity') + 1, cost = F('cost') + prod_price
        )
    if op == 'minus':
        C = Cart.objects.get(cart_no=request.session['cart_no'], product_id=pid)
        if C.quantity >= 2:
            C.quantity = F('quantity') - 1
            C.cost = F('cost') - prod_price
            C.save()
            
    return redirect('cart')


def success(request):
    return render(request, 'order_done.html')


def search(request):
    if request.method == "POST":
        if not check_required(request, ['key']):
            key = set_validate(request, 'key', sanitize=True)
            products = Products.objects.filter(name__icontains=key).exclude(status='hidden')
            return render(request, 'search.html', {"products": products, "key": key})
        else:
            return render(request, 'search.html')
    else:
        return render(request, 'search.html')


def contact(request):
    return render(request, 'contact.html')


def shop(request):
    prod = Products.objects.all()
    return render(request, 'products.html', {"prods": prod})


def pp(request):
    return render(request, 'privacy.html')


def about(request):
    return render(request, 'about.html')
