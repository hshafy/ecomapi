
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField, PrimaryKeyRelatedField

from products.models import Product, ProductGroup, ProductProperty


class ProductPropertySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductProperty
        #fields = ('url', 'key', 'value')

class ProductSerializer(HyperlinkedModelSerializer):
	properties = ProductPropertySerializer(
		many=True,
		read_only=True,
	  	)
	class Meta:
		model = Product
		#fields = ('url', 'product_variation', 'goss_price', 'tax', 'stock', 'properties')

class ProductGroupSerializer(HyperlinkedModelSerializer):
	products = ProductSerializer(
		many=True,
		read_only=True,
      	)
	class Meta:
		model = ProductGroup
		depth = 1
		fields = ('url', 'name', 'products')
