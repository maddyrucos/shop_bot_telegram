from django.db import models

class User(models.Model):
	user_id = models.IntegerField(primary_key=True,  verbose_name='Telegram ID')
	username = models.CharField(blank=True, verbose_name='Telegram Username', max_length=20)
	name = models.CharField(max_length=20 ,blank=True, verbose_name='Имя')
	balance = models.FloatField(default=0, verbose_name='Баланс')
	date_of_registration = models.DateField(auto_now_add=True)
	sales = models.ManyToManyField('Sale', related_name='sales', verbose_name='Покупки', blank=True)
	payments = models.ManyToManyField('Payment', related_name='payments', verbose_name='Платежи', blank=True)

	class Meta:
		verbose_name='Пользователь'
		verbose_name_plural='Пользователи'

	def __str__(self):
		return str(self.username)


class Categories(models.Model):
	path = models.CharField(verbose_name='Категория', max_length=100)

	class Meta:
		verbose_name='Категория'
		verbose_name_plural='Категории'

	def __str__(self):
		return str(self.path)


class Product(models.Model):
	name = models.CharField(verbose_name='Название товара', max_length=100)
	is_active = models.BooleanField(default=True, verbose_name='Включен')
	cost = models.FloatField(verbose_name='Цена')
	description = models.TextField(verbose_name='Описание')
	categories = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
	photo = models.ImageField(verbose_name='Фото')
	is_counted = models.BooleanField(default=False, verbose_name='Несколько')
	successful_payment_answer = models.ManyToManyField('Good', verbose_name='После оплаты')
	date_added = models.DateField(auto_now=True)

	class Meta:
		verbose_name='Товар'
		verbose_name_plural='Товары'

	def __str__(self):
		return str(self.name)


class Good(models.Model):
	#name = models.ForeignKey(Product, related_name='good_name', on_delete=models.CASCADE, verbose_name='Товар')
	is_unlimited = models.BooleanField(default=False, verbose_name='Бесконечный')
	data = models.TextField(verbose_name='Содержимое')

	class Meta:
		verbose_name='Содержимое'
		verbose_name_plural='Содержимое'

	def __str__(self):
		return str(self.data)


class PaymentMethod(models.Model):
	name = models.CharField(verbose_name='Название', max_length=50)
	callback = models.CharField(max_length=20)
	is_active = models.BooleanField(default=False, verbose_name='Активен')
	description = models.TextField(verbose_name='Описание (для пользователя)')
	api_key = models.CharField(verbose_name='API KEY', max_length=100, blank=True)
	extra = models.CharField(verbose_name='Доп. информация', max_length=100, blank=True)

	class Meta:
		verbose_name='Способ оплаты'
		verbose_name_plural='Способы оплаты'

	def __str__(self):
		return str(self.name)


class Payment(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
	amount = models.FloatField(verbose_name='Количество')
	method = models.ForeignKey(PaymentMethod, on_delete=models.DO_NOTHING, default=1, verbose_name='Способ оплаты')
	status = models.CharField(choices=[('waiting', 'Не оплачено'),
									   ('paid','Оплачено'),
									   ('canceled','Отменено')], verbose_name='Статус', max_length=20)
	date = models.DateField(auto_now=True, verbose_name='Дата')

	class Meta:
		verbose_name='Платеж'
		verbose_name_plural='Платежи'

	def __str__(self):
		return str(self.id)


class Sale(models.Model):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
	count = models.FloatField(verbose_name='Количество')
	cost = models.FloatField(verbose_name='Стоимость')
	date = models.DateField(auto_now=True, verbose_name='Дата')
	status = models.CharField(choices=[('waiting', 'waiting'), ('paid', 'paid'), ('canceled', 'canceled')], max_length=10, verbose_name='Статус')

	class Meta:
		verbose_name='Покупка'
		verbose_name_plural='Покупки'

	def __str__(self):
		return str(self.id)