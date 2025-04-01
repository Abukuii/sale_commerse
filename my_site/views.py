from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View  # Class-based views uchun
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from .models import Cart, CartItem, Product, Debtors
import json
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
            return redirect("home")  # Asosiy sahifaga yo‘naltirish
        else:
            messages.error(request, "Username yoki parol noto‘g‘ri!")
    return render(request, "login.html")

# Logout funksiyasi
def user_logout(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz!")
    return redirect("login")


# Asosiy sahifa (faqat login bo‘lgan foydalanuvchilar ko‘radi)
@login_required
def home(request):
    return render(request, "index.html")


# Foydalanuvchi login qilmagan bo‘lsa, barcha sahifalar bloklanadi
class ProtectedView(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args, **kwargs)


@login_required
def product_list(request):
    query = request.GET.get('q', '')  # Qidiruv so‘rovini olish
    products = Product.objects.all()  # Barcha mahsulotlarni olish
    if query:
        products = products.filter(name__icontains=query)  # Qidiruv bo‘yicha filterlash
    for product in products:
        product.sold_quantity = product.total_quantity - product.remaining_quantity
        product.save()
    return render(request, 'index2.html', {'products': products, 'query': query})


@login_required
def low_stock_products(request):
    """ Omborda kam qolgan mahsulotlarni chiqarish """
    query = request.GET.get('q', '')  # Qidiruv so‘rovini olish
    products = Product.objects.all()

    # 🔹 Qolgan miqdor minimal miqdordan kam bo'lgan mahsulotlarni tanlash
    low_stock_products = [product for product in products if product.remaining_quantity <= product.min_quantity]
    # 🔹 Qidiruv so‘ziga mos mahsulotlarni filterlash
    if query:
        low_stock_products = [product for product in low_stock_products if query.lower() in product.name.lower()]
    return render(request, 'index3.html', {'low_stock_products': low_stock_products, 'query': query})


@login_required
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Barcha mahsulotlar sahifasiga qaytish
    else:
        form = ProductForm()
    products = Product.objects.all()
    for product in products:
        product.sold_quantity = product.total_quantity - product.remaining_quantity
        product.save()
    return render(request, 'add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product,)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Tahrirlangandan keyin sahifaga qaytadi
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')  # O‘chirilgandan keyin sahifaga qaytadi


def debtors(request):
    """ Qarzdorlar ro‘yxatini chiqarish """
    debtors = Debtors.objects.all()
    return render(request, 'index4.html', {'debtors': debtors})



@login_required
def trade_product(request):
    query = request.GET.get('q', '')  # Qidiruv so‘rovini olish
    products = Product.objects.filter(name__icontains=query)  # Qidiruv bo‘yicha filterlash
    return render(request, 'index1.html', {'products': products, 'query': query})


# @login_required
# def get_cart(request):
#     """ Foydalanuvchining savatchasini ko‘rsatish """
#     cart, _ = Cart.objects.get_or_create(user=request.user)
#     cart_items = cart.items.all()
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#
#     return render(request, 'main/cart.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })
#
# @require_POST
# @login_required
# def add_to_cart(request, product_id):
#     """ Mahsulotni savatchaga qo‘shish """
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))
#
#     if product.remaining_quantity < quantity:
#         return JsonResponse({'error': 'Mahsulot yetarli emas!'}, status=400)
#
#     cart, _ = Cart.objects.get_or_create(user=request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#
#     if not created:
#         cart_item.quantity += quantity
#     else:
#         cart_item.quantity = quantity
#     cart_item.save()
#
#     return redirect('trade')
#
# @require_POST
# @login_required
# def update_cart(request, product_id, action):
#     """ Savatchadagi mahsulot sonini oshirish yoki kamaytirish """
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
#
#     if action == 'increment':
#         cart_item.quantity += 1
#         cart_item.save()
#     elif action == 'decrement':
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     elif action == 'remove':
#         cart_item.delete()
#
#     return redirect('trade')
#
# @require_POST
# @login_required
# def remove_from_cart(request, product_id):
#     """ Savatchadan mahsulotni butunlay o‘chirish """
#     cart = get_object_or_404(Cart, user=request.user)
#     try:
#         cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
#         cart_item.delete()
#     except CartItem.DoesNotExist:
#         return JsonResponse({'error': 'Mahsulot topilmadi!'}, status=404)
#
#     return redirect('trade')
#
# @require_POST
# @login_required
# def accept_purchase(request):
#     """ Sotib olishni tasdiqlash va ombordagi mahsulotlarni kamaytirish """
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = cart.items.all()
#
#     if not cart_items.exists():
#         return redirect('trade')
#
#     try:
#         for cart_item in cart_items:
#             product = get_object_or_404(Product, id=cart_item.product.id)
#             product.remaining_quantity -= cart_item.quantity
#             product.save()
#             cart_item.delete()
#
#         return redirect('trade')
#     except Product.DoesNotExist:
#         return JsonResponse({'error': 'Mahsulot topilmadi!'}, status=400)

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    # Получаем товар по его ID
    product = get_object_or_404(Product, id=product_id)

    # Проверяем, что количество товара в корзине достаточно для добавления
    if product.remaining_quantity < quantity:
        return JsonResponse({'error': 'Недостаточное количество товара в наличии'}, status=400)

    # Получаем или создаем корзину пользователя
    cart, created = Cart.objects.get_or_create()

    # Получаем или создаем товар в корзине
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('trade')


@require_POST
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            cart_item = CartItem.objects.get(product_id=product_id)
            cart_item.delete()
            return redirect('cart')
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Товар не найден'}, status=404)
    else:
        return JsonResponse({'error': 'Метод запроса должен быть POST'}, status=400)


def get_cart(request):
    # Получаем или создаем корзину
    cart, created = Cart.objects.get_or_create()

    # Получаем все товары в корзине пользователя
    cart_items = cart.items.all()

    # Рассчитываем общую стоимость корзины
    total_price = sum(item.product.sell_price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@require_POST
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        increment = request.POST.get('increment')
        decrement = request.POST.get('decrement')
        remove = request.POST.get('remove')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Товар не найден'}, status=404)

        cart, created = Cart.objects.get_or_create()

        # Увеличение количества товара
        if increment:
            cart_item, item_created = cart.items.get_or_create(product=product)
            cart_item.quantity += 1
            cart_item.save()

        # Уменьшение количества товара
        elif decrement:
            cart_item, item_created = cart.items.get_or_create(product=product)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        # Удаление товара
        elif remove:
            try:
                cart_item = cart.items.get(product=product)
                cart_item.delete()
            except CartItem.DoesNotExist:
                pass

        return redirect('get_cart')


def accept_purchase(request):
    if request.method == 'POST':
        # Получаем все товары в корзине пользователя
        cart_items = CartItem.objects.all()

        # Проверяем наличие товаров в корзине
        if cart_items.exists():
            try:
                # Обновляем количество товаров в базе данных и очищаем корзину
                for cart_item in cart_items:
                    product = get_object_or_404(Product, id=cart_item.product.id)
                    product.remaining_quantity -= cart_item.quantity
                    product.sold_quantity = product.total_quantity - product.remaining_quantity
                    product.save()
                    cart_item.delete()

                # Возвращаем успешный ответ в формате JSON
                return redirect('trade')

            except Product.DoesNotExist:
                # Если продукт не найден, возвращаем ошибку в формате JSON
                return JsonResponse({'success': False, 'error': 'Product not found'})

    # Если корзина пуста или метод запроса не POST, перенаправляем пользователя обратно на страницу корзины
    return redirect('cart')


# def delete_product(request, product_id):
#     if request.method == 'POST':
#         try:
#             product = Product.objects.get(id=product_id)
#             product.delete()
#             messages.success(request, 'Product deleted successfully')
#         except Product.DoesNotExist:
#             messages.error(request, 'Product not found')
#     return redirect(reverse('all_products'))














# @login_required
# @require_POST
# def add_to_cart(request):
#     product_id = request.POST.get('product_id')
#     quantity = int(request.POST.get('quantity', 1))
#
#     product = get_object_or_404(Product, id=product_id)
#
#     if product.quantity < quantity:
#         return JsonResponse({'error': 'Yetarli mahsulot yo‘q'}, status=400)
#
#     cart, created = Cart.objects.get_or_create(user=request.user)
#
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
#     cart_item.quantity += quantity if not item_created else quantity
#     cart_item.save()
#
#     return redirect('trade')
#
#
# @login_required
# @require_POST
# def remove_from_cart(request):
#     product_id = request.POST.get('product_id')
#
#     try:
#         cart_item = CartItem.objects.get(cart__user=request.user, product_id=product_id)
#         cart_item.delete()
#         return redirect('trade')
#     except CartItem.DoesNotExist:
#         return JsonResponse({'error': 'Tovar topilmadi'}, status=404)
#
#
# @login_required
# @require_POST
# def accept_purchase(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     cart_items = cart.items.all()
#
#     if cart_items.exists():
#         for cart_item in cart_items:
#             product = cart_item.product
#             if product.quantity >= cart_item.quantity:
#                 product.quantity -= cart_item.quantity
#                 product.save()
#                 cart_item.delete()
#             else:
#                 return JsonResponse({'error': 'Yetarli mahsulot yo‘q'}, status=400)
#
#         return redirect('trade')
#
#     return redirect('trade')
