from django.urls import path
from api.views import *

app_name='api'

urlpatterns = [
    path('products/', api_products, name='products'),
    path('products/<int:product_id>', api_products_detail, name='product'),
    path('sales/', api_sales, name='sales'),
    path('sales/<int:sale_id>', api_sales_detail, name='sale'),
    path('goods/', api_goods, name='goods'),
    path('goods/<int:product_id>', api_goods_detail, name='good'),
]