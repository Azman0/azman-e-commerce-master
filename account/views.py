from django.shortcuts import render, redirect
from .models import Clients, Orders
from django.contrib import messages
from django.db.models import Sum
from web.models import Cart
import datetime
import random
import string
import hashlib


def logged_in(request):
    try:
        return request.session['client_id']
    except KeyError:
        return False


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

# Create your views here.


def login(request):
    if logged_in(request):
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        if not check_required(request, ['email', 'password']):
            email = set_validate(request, 'email', sanitize=True)
            try:
                C = Clients.objects.get(email = email)
                password = hashlib.md5(bytes(request.POST['password'], "ascii")).hexdigest()
                if C.password == password:
                    request.session['client_id'] = C.id
                    return redirect('index')
                else:
                    messages.error(request, 'PASSWORD DOES NOT MATCH')
                    return redirect('login')
            except:
                messages.error(request, 'USER DOES NOT EXISTS')
                return redirect('login')
        else:
            messages.error(request, 'SOME REQUIRED FIELD MISSING')
    else:
        return redirect('login')


def register(request):
    if logged_in(request):
        return redirect('index')

    if request.method == 'GET':
        return render(request, 'signup.html')

    elif request.method == 'POST':
        if not check_required(request, ['full_name', 'email', 'password1', 'password2']):
            if request.POST['password1'] == request.POST['password2']:
                email = set_validate(request, 'email', sanitize=True)
                if Clients.objects.filter(email=email):
                    messages.error(request, 'ALREADY HAVE AN ACCOUNT USING THIS EMAIL ADDRESS')
                    return redirect('register')
                else:
                    password = hashlib.md5(bytes(request.POST['password1'], "ascii")).hexdigest()
                    C = Clients (
                        full_name = set_validate(request, 'full_name', sanitize=True),
                        email = request.POST['email'],
                        password = password,
                    )
                    C.save()
                    # request.session['client_id'] = C.id
                    messages.success(request, 'REGISTRATION SUCCESSFULL')
                    return redirect('login')
            else:
                messages.error(request, 'TWO PASSWORD DOES NOT MATCH')
                return redirect('register')
        else:
            messages.error(request, 'SOME REQUIRED FIELD MISSING')
            return redirect('register')
    else:
        return None


def myaccount(request):
    if not logged_in(request):
        return redirect('login')
    else:
        client_id = request.session['client_id']
    
    if request.method == "GET":
        client = Clients.objects.get(id=client_id)
        return render(request, 'account/profile.html', {"client": client})
    
    elif request.method == "POST":
        try:
            full_name = request.POST['full_name']
            address = set_validate(request, 'address', sanitize=True)
            pupdate = Clients.objects.filter(id=client_id).update(full_name=full_name, address=address)
            if pupdate:
                messages.success(request, 'PROFILE UPDATED SUCCESSFULLY')
            return redirect('myaccount')
        except:
            pass

        try:
            if not check_required(request, ['old_password', 'new_password', 'confirm_password']):
                old_password = hashlib.md5(bytes(request.POST['old_password'], "ascii")).hexdigest()
                new_password = hashlib.md5(bytes(request.POST['new_password'], "ascii")).hexdigest()
                confirm_password = hashlib.md5(bytes(request.POST['confirm_password'], "ascii")).hexdigest()

                if new_password == confirm_password:
                    client = Clients.objects.get(id=client_id)
                    if client.password == old_password:
                        Clients.objects.filter(id=client_id).update(password=new_password)
                        messages.success(request, 'PASSWORD SUCCESSFULLY CHANGED!')
                    else:
                        messages.error(request, 'OLD PASSWORD DOES NOT MATCH')
                        return redirect('myaccount')
                else:
                    messages.error(request, 'TWO PASSWORD DOES NOT MATCH')
                    return redirect('myaccount')
            else:
                messages.error(request, 'REQUIRED FIELD MISSING!')
        except:
            pass
        return redirect('myaccount')
    else:
        return None


def myorders(request):
    if not logged_in(request):
        return redirect('login')
    else:
        client_id = request.session['client_id']

    orders = Orders.objects.filter(client_id = client_id).order_by('-id')
    return render(request, 'account/myorders.html', {"orders": orders})


def orderdetails(request, cart_no):
    if not logged_in(request):
        return redirect('login')
    else:
        client_id = request.session['client_id']

    order = Orders.objects.get(cart_no=cart_no)
    orderdtl = Cart.objects.select_related('product_id').filter(cart_no=cart_no)
    return render(request, 'account/orderdetails.html', { "order": order, "orderdtl": orderdtl })


def logout(request):
    try:
        del request.session['client_id']
    except:
        pass

    messages.error(request, "Logged Out!")
    return redirect('login')


def confirmorder(request):
    if not logged_in(request):
        messages.error(request, 'PLEASE LOGIN / REGISTER TO CONFIRM ORDER!')
        return redirect('login')
    else:
        client_id = request.session['client_id']
    
    try:
        request.session['cart_no']
    except:
        return redirect('index')

    if request.method == "GET":
        try:
            client = Clients.objects.get(id=client_id)
        except:
            return redirect('login')
        return render(request, 'order_form.html', {"client": client} )
    
    elif request.method == "POST":
        cost = Cart.objects.filter(cart_no=request.session['cart_no'])
        pcost = 0
        for item in cost:
            pcost += item.cost
        
        if pcost >= 1:
            delivery_fees = 20
        else:
            delivery_fees = 0

        total_cost = pcost + delivery_fees
        created_at = datetime.datetime.now()
        order_no = request.session['cart_no']
        # Minimum total cost for a shopping or if no cart but hitted order
        if total_cost <= 0:
            return redirect('index')

        Orders.objects.create(
            cart_no = request.session['cart_no'],
            order_no = order_no,
            client_id = client_id,
            full_name = set_validate(request, 'full_name', sanitize=True),
            mobile = set_validate(request, 'mobile', sanitize=False),
            address = set_validate(request, 'address', sanitize=True),
            cost = pcost,
            delivery_fees = delivery_fees,
            total_cost = total_cost,
            created_at = created_at
        )
        del request.session['cart_no']
        return redirect('success')  # will be redirect to a order confirm page
    else:
        return None

