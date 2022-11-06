from django.contrib import admin
from Home.models import Contact, Order_location, Our_collection, Our_customer, customer_orders, orders_cart, order_updates

# Register your models here.
admin.site.register(Contact)
admin.site.register(Order_location)
admin.site.register(Our_collection)
admin.site.register(Our_customer)
admin.site.register(customer_orders)
admin.site.register(orders_cart)
admin.site.register(order_updates)
