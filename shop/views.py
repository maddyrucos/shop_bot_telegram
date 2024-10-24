from django.shortcuts import render
from shop.models import *

def index(request):
    goods = Product.objects.filter(is_active=True).order_by('-date_added')[:10]
    context = {'last_goods': goods}
    return render(request, 'shop/index.html', context=context)
