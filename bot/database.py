from bot_shop.models import User, Product, Payment, Categories, Sale, PaymentMethod, Good

def create_profile(user_id, username):
	user = User.objects.update_or_create(user_id=user_id, defaults={"user_id":user_id, "username":username})


def get_user_by_id(user_id):
	try:
		return User.objects.get(user_id=user_id)
	except Exception as e:
		print(Exception)
		return None


def change_balance(user: User, amount):
	try:
		user.balance -= amount
		user.save()
		return True
	except Exception as e:
		print(e)
		return False


def get_categories(path, iteration):
	try:
		pathes = Categories.objects.filter(path__startswith=path)
		categories = []
		for cat in pathes:
			category = cat.path.split('_')
			category = category[iteration]
			categories.append(category)
		iteration+=1

		return set(categories), iteration

	except IndexError:
		category=Categories.objects.get(path=path)
		products = Product.objects.filter(categories=category, is_active=True)
		prod_list = []
		for product in products:
			prod_list.append(product.name)

		return prod_list, 'product'


def get_product(product_name, path):
	category = Categories.objects.get(path=path)
	try:
		product = Product.objects.get(name=product_name, categories=category)
		return product
	except:
		return 0


def create_sale(user, product, count, cost):
	try:
		return Sale.objects.create(customer=user, product=product, count=count, cost=cost, status=0)
	except Exception as e:
		print(e)
		return False


def get_sale(user: User, product: Product, count: float, cost: float, status=0):
	try:
		return Sale.objects.filter(customer=user, product=product, count=count, cost=cost, status=status).last()
	except Exception as e:
		print(e)
		return None


def change_sale_status(sale: Sale, status):
	try:
		sale.status = status
		sale.save()
		return True
	except Exception as e:
		print(e)
		return False

def create_transaction():
	pass


def get_profile(user_id):
	user = get_user_by_id(user_id)
	sales = user.sales
	count = sales.count()
	try:
		last_sale = Sale.objects.filter(user.sales).last()
	except:
		last_sale = 0
	return {
			'username': user.username,
			'sales': count,
			'last_sale': last_sale
			}

def get_topup_methods():
	return PaymentMethod.objects.filter(is_active=True)


def get_topup_method(callback):
	return PaymentMethod.objects.get(callback=callback)


def get_good(product):
	return product.successful_payment_answer.first()


def delete_good(good):
	if not good.is_unlimited:
		good.delete()


def get_payment_info(method):
	try:
		return PaymentMethod.objects.get(callback=method)
	except Exception as e:
		print(e)
		return None

