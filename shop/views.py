from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from shop.models import *


def index(request):
    products = Product.objects.filter(is_active=True).order_by('date_added')[:10]
    context = {'last_products': products}
    return render(request, 'shop/index.html', context=context)


def product(request, product_id):

    return render(request, 'shop/product_page.html')


@login_required()
def product_buy(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = get_object_or_404(User, username=request.user)
    content = Product.successful_payment_answer.first()
    context = { 'product': product, 'user': user, 'content': content }
    return JsonResponse(context)


def catalog(request, path=''):
    if path:
        categories = Category.objects.filter(path__istartswith=path)
        categories_path = [category['path'].split('_') for category in categories]
        context = { 'categories': categories_path, 'first': False }
    else:
        categories = Category.objects.all().values('path')
        categories_path = [category['path'] for category in categories]
        context = { 'categories': categories_path, 'first': True }
    return render(request, 'shop/catalog.html', context=context)


def search(request):
    query=request.GET.get('q')
    results = Product.objects.filter(name__icontains=query).values('id', 'name')
    return JsonResponse({'results': list(results)})