
from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path('home', views.home, name='Home'),
    path('', views.index, name='index'),
    path("about", views.about, name='About'),
    path("services", views.services, name='Services'),
    path("contact", views.contact, name='Contact'),
    path("collection", views.collection, name='Collection'),
    path("customer", views.customer, name='Customer'),
    path("register", views.register, name='Register'),
    path("logout", views.logout, name='logout'),
    path("Profile", views.profile, name='profile'),
    path("Cart", views.Cart, name='Cart'),
    path("tracking", views.tracker, name='tacking'),
    path("removecart", views.removecart, name='removecart'),
    path("orders", views.orders, name='orders'),
    path("mywebcss", views.mywebcss, name='mywebcss'),
    path("addcart", views.addcart, name='addcart'),
    path("addlocation", views.addlocation, name='addlocation'),
    path("order", views.order, name='order'),
    path("cancelorder", views.cancelorder, name="cancelorder"),
    path("updatepassword", views.updatepassword, name="updatepassword"),






]
