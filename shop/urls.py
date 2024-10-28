from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:product_id>/buy', views.product_buy, name='buy_product')
]