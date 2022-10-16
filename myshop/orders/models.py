from django.db import models
from shop.models import Product
import secrets
from .paystack import PayStack
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.urls import reverse
from django.contrib.auth.models import User
from cart.cart import Cart

class Order(models.Model):
    STATUS = [
        ('Dala', ('Dala')),
        ('Fagge', ('Fagge')),
        ('Kano municipal', ('Kano municipal')),
        ('Kumbotso', ('Kumbotso')),
        ('Nassarawa', ('Nassarawa')),
        ('Rimi', ('Rimi')),
        ('Tarauni', ('Tarauni')),
        ('Ungogo', ('Ungogo')),
    ]
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100, choices=STATUS, default='NASSARAWA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    ref = models.CharField(max_length=200)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(10)
            object_with_similar_ref = Order.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)


    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100)) + self.shipping() + self.service_fee()

    def service_fee(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        a = (total_cost)*(Decimal(5)/Decimal(100))
        c = round(a, 2)
        return c

    def shipping(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        if total_cost >= 30000:
            shipping_cost = 0
        elif total_cost in range(25000, 30000):
            shipping_cost = 2000
        elif total_cost in range(20000, 2500):
            shipping_cost = 1500
        elif total_cost in range(10000, 20000):
            shipping_cost = 1000
        elif total_cost in range(5000, 10000):
            shipping_cost = 750
        elif total_cost in range(1, 5000):
            shipping_cost = 500
        else:
            shipping_cost = 0
        return shipping_cost

    def amount_value(self) -> int:
        return self.get_total_cost()*100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.get_total_cost())
        if status:
            if result['amount'] / 100 == self.get_total_cost():
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False

    def get_absolute_url(self):
        return reverse('account:order_details', args=[self.id])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def get_absolute_url(self):
        return self.product.get_absolute_url()