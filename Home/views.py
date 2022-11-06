from django.shortcuts import render, HttpResponse, redirect
from Home.models import Contact, Order_location, Our_collection, Our_customer, customer_orders, orders_cart, order_updates
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
import random
import json

from django.contrib import auth


# Create your views here.

# Index page function ****************************************

username = None


def index(request):
    global username
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        users = list(Our_customer.objects.values('firstname'))
        passwords = list(Our_customer.objects.values('password'))
        u = []
        p = []
        user_pass = {}

        for x in users:
            u.append(x['firstname'])

        for y in passwords:
            p.append(y['password'])

        for i in range(len(u)):
            user_pass.setdefault(u[i], p[i])
        # authentication
        if username in user_pass:
            val = user_pass[username]

            if val == password:
                request.session['username'] = username
                messages.success(request, 'Log in successfully!')

                return render(request, 'home.html', {"username": username})

        else:
            user = auth.authenticate(
                request, username=username, password=password)
            if user is not None:

                auth.login(request, user)
                request.session['username'] = username
                messages.success(request, 'Log in successfully!')

                return render(request, 'home.html', {"username": username})

            else:
                messages.error(request, 'log in  unsuccessfull!')
                return render(request, 'index.html')

    return render(request, 'index.html')

  #  return HttpResponse("this is homepage")

# Home Page function *********************************************


def home(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x

    request.session['username'] = username

    cart_items = orders_cart.objects.all().filter(username=username).count()
    count = orders_cart.objects.all().filter(username=username).count()
    return render(request, 'home.html', {"count": count, "username": username, "cart_items": cart_items})

# About function************************************************


def about(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x

    request.session['username'] = username

    cart_items = orders_cart.objects.all().filter(username=username).count()
    count = orders_cart.objects.all().filter(username=username).count()

    return render(request, 'about.html', {"count": count, "username": username, "cart_items": cart_items})

# Service function **********************************************


def services(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x

    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()

    icecreams = Our_collection.objects.all()
    paginator = Paginator(icecreams, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'services.html', {'page_obj': page_obj, "count": count, "username": username})


def addlocation(request):

    if request.method == 'POST':
        user = request.POST.get('user')

        print(user)
        username = ""
        for x in user:
            if x.isalpha():
                username += x

        request.session['username'] = username
        cart_items = orders_cart.objects.all().filter(username=username)
        count = orders_cart.objects.all().filter(username=username).count()
        icecreams = Our_collection.objects.all()
        paginator = Paginator(icecreams, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        location = request.POST.get('location')
        services = Order_location(location=location)
        print(location)
        services.save()

        messages.success(
            request, "your location has been save. Now select icecream..")
        return render(request, 'services.html', {'page_obj': page_obj, "count": count, "username": username})

    else:
        logout(request)
        messages.error(
            request, "Something happend wrong !.Please login again and Try..")
        return render(request, 'index.html')


# Contact function ***********************************************


def contact(request):

    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        print(name)
        contact = Contact(name=name, email=email, phone=phone,
                          desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent successfully!')

    # return HttpResponse("this is Contactspage")
    return render(request, 'contact.html', {"count": count, "username": username, "cat_items": cart_items})

# Collection function*************************************************


def collection(request):

    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()

    icecreams = Our_collection.objects.all()
    return render(request, 'collection.html', {'icecreams': icecreams, "count": count, "username": username})

# Customer Function ***************************************************


def customer(request):

    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()

    icecream_id = request.GET.get('icecream_id')
    item = request.GET.get('item')

    return render(request, 'customer.html', {'icecream_id': icecream_id, 'cart_items': cart_items, 'item': item, "count": count, "username": username})

# REgisteration function*******************************************


def register(request):

    count = orders_cart.objects.all().count()

    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        user = request.POST.get("user")

        # check for errrorneous inputs
        if len(email) > 100:
            messages.error(request, "username must be under 100 characters")
            return redirect("/")
        if password != confirmpassword:
            messages.error(
                request, "passwords do not match !!!!!!!")
            return redirect('/')

         # add into our_coustomer table
        register = Our_customer(
            firstname=firstname, lastname=lastname, username=email, password=password)
        register.save()

        # Create  the user
        if user == "superuser":

            my_user = User.objects.create_user(firstname, email, password)
            my_user.first_name = firstname
            my_user.last_name = lastname
            my_user.save()

        messages.success(
            request, 'Your account has been created successfully! your firstname will be username .')

    else:

        return HttpResponse('404- Not Found')

    return render(request, 'index.html', {"count": count})

# Log Out function**************************************************


def logout(request):
    auth.logout(request)
    try:
        del request.session['username']
    except:
        pass
    messages.success(request, 'Loged out successfully!')

    return render(request, 'index.html')

# Profile function**************************************************


def profile(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().count()

    customers = Our_customer.objects.all().filter(firstname=user)
   # print(customer)

    return render(request, 'profile.html', {"count": count, "customers": customers, "username": username})

# Cart function*********************************************************


def Cart(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username__contains=user)
    count = orders_cart.objects.all().count()

    return render(request, 'cart.html', {"cart_items": cart_items, "count": count, "username": username})

# Add to Cart Function **************************************************


def addcart(request):
    user = request.GET.get("username")

    username = ""
    for x in user:
        if x.isalpha():
            username += x

    # print(username)
    request.session['username'] = username
    if request.method == 'GET':
        icecream_id = (request.GET.get('icecream_id')).rsplit(",")
        for ids in icecream_id:
            cart_id = Our_collection.objects.filter(icecream_id=ids)
            for i in cart_id:
                icecream_id = i.icecream_id
                icecream_name = i.icecream
                icecream_image = i.icecream_img
                icecream_price = i.price
                cart = orders_cart(icecream_id=icecream_id, icecream_name=icecream_name, username=username,
                                   icecream_image=icecream_image, icecream_price=icecream_price)
                cart.save()
        messages.success(
            request, "Succesfully Add to cart..")
        cart_items = orders_cart.objects.all().filter(username=username)
        count = orders_cart.objects.all().count()

    return render(request, 'cart.html', {"cart_items": cart_items, "count": count, "username": username})

# RemoveCart Function***************************************************


def removecart(request):
    user = request.GET.get("username")
    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username

    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item = orders_cart.objects.get(cart_id=item_id)
        item.delete()
        cart_items = orders_cart.objects.all().filter(username=username)
        count = orders_cart.objects.all().count()

        return render(request, 'cart.html', {"count": count, "cart_items": cart_items, "username": username})

# Track order function*************************************************


def tracker(request):
    user = request.GET.get("username")

    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()
    if request.method == "POST":

        order_id = request.POST.get('order_id', '')
        mobile_no = request.POST.get('mobile_no', '')

        try:
            order = customer_orders.objects.filter(
                order_id=order_id, mobile_no=mobile_no
            )
            # print(len(order))
            if len(order) > 0:
                update = order_updates.objects.filter(
                    order_id=order_id)
                percentage = order_updates.objects.all().last()
                per = int(percentage.update_percentage)
                print(update)
                print(per)
                print("---", percentage)

                if per == None:
                    messages.warning(
                        request, "No update found!!!")

                    return render(request, 'tracker.html', {"update": update, "per": per, "cart_items": cart_items, "count": count, "username": username})
                elif per > 0 and per <= 10:
                    messages.success(
                        request, "Your has been dispatched and it will be to your destinaton soon!!!!")

                    return render(request, 'tracker.html', {"update": update, "per": per, "cart_items": cart_items, "count": count, "username": username})
                elif per >= 25 and per <= 100:
                    messages.success(
                        request, "Your order is on the way and will be to your place soon!!!")

                    return render(request, 'tracker.html', {"update": update, "per": per, "cart_items": cart_items, "count": count, "username": username})

            else:
                return render(request, 'tracker.html', {"update": update, "per": per, "cart_items": cart_items, "count": count, "username": username})

        except Exception as e:
            return HttpResponse(f'exception {e}')

    return render(request, 'tracker.html', {"count": count, "cart_items": cart_items, "username": username})

# Orders function*******************************************************


def orders(request):
    user = request.GET.get("username")

    username = ""
    for x in user:
        if x.isalpha():
            username += x
    request.session['username'] = username
    cart_items = orders_cart.objects.all().filter(username=username)
    count = orders_cart.objects.all().filter(username=username).count()
    my_orders = customer_orders.objects.all().filter(name__contains=user)
    return render(request, 'order.html', {"count": count, "my_orders": my_orders, "cart_items": cart_items, "username": username})


# order function*******************************
def order(request):

    if request.method == 'POST':
        user = request.POST.get('user')
        username = ""
        for x in user:

            if x.isalpha():

                username += x
        request.session['username'] = username
        icecream_id = request.POST.get('icecream_id')
        order_item = request.POST.get('order_item')
        customer_name = request.POST.get('name')
        customer_address = request.POST.get('address')
        customer_phone = request.POST.get('phone')
        customer_pin = request.POST.get('pin')
        customer_distt = request.POST.get('distt')
        customer_state = request.POST.get('state')
        order_id = random.randint(10001, 100000001)
        cart_items = orders_cart.objects.all().filter(username=username)
        count = orders_cart.objects.all().filter(username=username).count()

        customer = customer_orders(order_id=order_id, order_item=order_item, name=customer_name, address=customer_address,
                                   distt=customer_distt, pin_code=customer_pin, state=customer_state, mobile_no=customer_phone)
        customer.save()
        # update = order_updates(order_id=customer.order_id,
        # update_desc="This order has been placed.")
        # update.save()
        messages.success(
            request, "Your order has been saved. Thanku for ordering items ..!!! check Your ordre in your order list.")

        return render(request, 'customer.html', {'icecream_id': icecream_id, 'cart_items': cart_items, "count": count, "username": username})
    else:
        return render(request, 'customer.html', {'icecream_id': icecream_id, 'cart_items': cart_items, "count": count, "username": username})


# myweb function********************************************************
def mywebcss(request):
    return render(request, 'myweb.css')


# cancel order function ***************************
def cancelorder(request):

    if request.method == 'GET':
        user = request.GET.get('username')
        username = ""
        for x in user:

            if x.isalpha():

                username += x
        request.session['username'] = username
        cart_items = orders_cart.objects.all().filter(username=username)
        count = orders_cart.objects.all().filter(username=username).count()

        order_id = request.GET.get('order_id')

        item = customer_orders.objects.get(order_id=order_id)
        item.delete()
        my_orders = customer_orders.objects.all()

    return render(request, 'order.html', {"count": count, "my_orders": my_orders, "cart_items": cart_items, "username": username})


# Update password ------------------------------------
def updatepassword(request):
    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        new_password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        user = request.POST.get("user")

        # check for errrorneous inputs
        if len(email) > 100:
            messages.error(request, "username must be under 100 characters")
            return redirect("/")
        if new_password != confirmpassword:
            messages.error(
                request, "passwords do not match !!!!!!!")
            return redirect('/')

        Our_customer.objects.filter(
            username=email).update(password=new_password)

        messages.success(
            request, "Your password has been update. Log In please!!!")

        return render(request, 'index.html')
    else:
        messages.error(
            request, "Your username not found !!")

        return render(request, 'index.html')


