
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField, PrimaryKeyRelatedField

from products.models import Product, ProductGroup, ProductProperty


class ProductPropertySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProductProperty
        #fields = ('url', 'key', 'value')

class ProductSerializer(HyperlinkedModelSerializer):
	"""
	Product Serializer with nested properties.

	Product can be created without properites, then properties can be assigned later.
	"""
	properties = ProductPropertySerializer(
		many=True,
		read_only=True,
	  	)
	class Meta:
		model = Product
		#fields = ('url', 'product_variation', 'goss_price', 'tax', 'stock', 'properties')

class ProductGroupSerializer(HyperlinkedModelSerializer):
	"""
	Product Group Serializer with nested products.

	ProductGroup can't be created without the nested products.
	"""
	products = ProductSerializer(
		many=True,
      	)
	class Meta:
		model = ProductGroup
		depth = 1
		fields = ('url', 'name', 'products')

	def create(self, validated_data):
		products_data = validated_data.pop('products')
		product_group = ProductGroup.objects.create(**validated_data)
		for product_data in products_data:
			Product.objects.create(product_group=product_group, **product_data)
		return product_group
