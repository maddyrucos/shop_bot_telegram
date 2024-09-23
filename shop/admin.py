from django.contrib import admin
from .models import *

models_list = [User, Good, Categories, Product, PaymentMethod, Payment, Sale]

for model in models_list:
    admin.site.register(model)
