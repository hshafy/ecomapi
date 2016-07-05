import uuid

from django.db import models

class ProductGroup(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Product(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product_variation = models.CharField(max_length=100)
	product_group = models.ForeignKey(ProductGroup, blank=True, related_name='products')
	goss_price = models.DecimalField(max_digits=8, decimal_places=2)
	tax = models.DecimalField(max_digits=4, decimal_places=4)
	stock = models.IntegerField()

class ProductProperty(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	product = models.ForeignKey(Product, related_name='properties')
	key = models.CharField(max_length=100)
	value = models.CharField(max_length=100)
