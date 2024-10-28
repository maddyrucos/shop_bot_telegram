from django.shortcuts import render, get_object_or_404
from shop.models import *

def index(request):
    products = Product.objects.filter(is_active=True).order_by('date_added')[:10]
    context = {'last_products': products}
    return render(request, 'shop/index.html', context=context)


def product_buy(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_anonymous:
        print('anon')
    else:
        print(request.user)

    return render(request, 'shop/product_page.html')

