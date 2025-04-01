from django.contrib import admin
from .models import Product, Debtors, Cart, CartItem

@admin.register(Product)  # Modelni ro‘yxatdan o‘tkazish va sozlash
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_quantity', 'sold_quantity', 'remaining_quantity', 'min_quantity', 'cost_price', 'sell_price', 'profit_margin', 'is_low_stock', 'image')
    search_fields = ('name',)  # Mahsulot nomi bo‘yicha qidirish

admin.site.register(Debtors)
admin.site.register(Cart)
admin.site.register(CartItem)
