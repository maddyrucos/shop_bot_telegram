from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.utils.representation import serializer_repr

from shop.models import Product, Good, Sale
from api.serializers import ProductSerializer, GoodSerializer, SaleSerializer


@api_view(['GET'])
def api_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_products_detail(request, product_id):
    event = Product.objects.get(product_id)
    if request.method == 'GET':
        serializer = ProductSerializer(event)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_sales(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_sales_detail(request, sale_id):
    sales = Sale.objects.get(sale_id)
    if request.method == 'GET':
        serializer = SaleSerializer(sales)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_goods(request):
    if request.method == 'GET':
        goods = Good.objects.all()
        serializer = GoodSerializer(goods, many=True)
        return Response(serializer.data)
    else:
        return Response(request, status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def api_goods_detail(request, good_id):
    goods = Product.objects.get(good_id)
    if request.method == 'GET':
        serializer = GoodSerializer(goods)
        return Response(serializer.data)
    else:
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)