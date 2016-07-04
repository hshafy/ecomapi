from django.db import models

class ProductGroup(models.Model):
	name = models.CharField(max_length=255)

class Product(models.Model):
	product_variation = models.CharField(max_length=100)
	product_group = models.ForeignKey(ProductGroup, blank=True, related_name='products')
	goss_price = models.DecimalField(max_digits=8, decimal_places=2)
	tax = models.DecimalField(max_digits=4, decimal_places=4)
	stock = models.IntegerField()

class ProductProperty(models.Model):
	product = models.ForeignKey(Product, related_name='properties')
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
