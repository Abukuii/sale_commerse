from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    total_quantity = models.IntegerField(default=0)
    remaining_quantity = models.PositiveSmallIntegerField( default=0)
    sold_quantity = models.IntegerField(default=0)
    min_quantity = models.IntegerField(default=5)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)  # O‘z narxi
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Sotish narxi
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Foyiz
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # 🔹 Rasm maydoni

    @property
    def is_low_stock(self):
        return self.remaining_quantity <= self.min_quantity

    def save(self, *args, **kwargs):
        if self.profit_margin and not self.sell_price:
            # Agar foyiz kiritilsa, sotish narxini hisoblaymiz
            self.sell_price = self.cost_price + (self.cost_price * self.profit_margin / 100)
        elif self.sell_price and not self.profit_margin:
            # Agar sotish narxi kiritilsa, foyizni hisoblaymiz
            self.profit_margin = ((self.sell_price - self.cost_price) / self.cost_price) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def get_total(self):
        total = self.product.sell_price * self.quantity
        return total

    def __str__(self):
        return self.cart

class Debtors(models.Model):
    full_name = models.CharField(max_length=250)
    phone_numuber = models.CharField(max_length=250)
    product = models.ManyToManyField(Product, blank=True)
    date = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.full_name























# class Sale(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} dona"