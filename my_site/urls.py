from django.urls import path
from .views import *
from .views import user_login, user_logout, home, ProtectedView, trade_product
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path("protected/", ProtectedView.as_view(), name="protected"),

    # ✅ Login va logout sahifalarini faqat bir marta qo‘shamiz
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),


    # ✅ Mahsulot sahifalari
    path('products/', product_list, name='product_list'),
    path('low-stock/', low_stock_products, name='low_stock_products'),
    path('add-product/', add_product, name='add_product'),
    path('edit/<int:pk>/', edit_product, name='edit_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),

    #  Trade Products
    # path('trade/', trade_product, name='trade'),
    # path('debetors', debetors, name='debetors'),
    # path('accept_purchase/', accept_purchase, name='accept_purchase'),
    # # path('notifacation/', notifacation, name='notifacation'),
    # path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # URL для добавления товара в корзину
    # path('cart/', get_cart, name='cart'),  # URL для страницы корзины
    # path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    # path('update_cart/', update_cart, name='update_cart'),
    # path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

    path('trade/', trade_product, name='trade'),
    path('debtors', debtors, name='debtors'),
    path('accept_purchase/', accept_purchase, name='accept_purchase'),
    # path('all_products/', all_products, name='all_products'),
    # path('notifacation/', notification, name='notifacation'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),  # URL для добавления товара в корзину
    path('cart/', get_cart, name='cart'),  # URL для страницы корзины
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

