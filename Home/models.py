from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)

    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Order_location(models.Model):
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.location


class Our_collection(models.Model):
    icecream_id = models.IntegerField()

    icecream = models.CharField(max_length=200)
    icecream_img = models.FileField()
    price = models.IntegerField()

    def __str__(self):
        return self.icecream


class Our_customer(models.Model):

    firstname = models.CharField(max_length=200, unique=False)
    lastname = models.CharField(max_length=200)
    username = models.EmailField(max_length=200)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname


class customer_orders(models.Model):

    order_id = models.IntegerField(primary_key=True)
    order_item = models.CharField(max_length=200)
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=200)
    pin_code = models.IntegerField()
    distt = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    mobile_no = models.IntegerField(max_length=12)

    def __str__(self):
        return self.name


class orders_cart(models.Model):

    cart_id = models.AutoField(primary_key=True)
    icecream_id = models.IntegerField()
    icecream_name = models.CharField(max_length=200)
    username = models.CharField(max_length=40)
    icecream_image = models.FileField(max_length=200)
    icecream_price = models.IntegerField()

    def __str__(self):
        return self.icecream_name


class order_updates(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=500)
    update_percentage = models.IntegerField()

    def __str__(self):
        return self.update_desc[0:7] + "..."
