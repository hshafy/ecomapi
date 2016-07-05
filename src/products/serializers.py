
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField, PrimaryKeyRelatedField

from products.models import Product, ProductGroup, ProductProperty


class RelatedProductPropertySerializer(HyperlinkedModelSerializer):
	"""
	Product Property Serializer to be included in the Product Represetation
	"""
	class Meta:
		model = ProductProperty
		fields = ['url', 'key', 'value']

class ProductPropertySerializer(HyperlinkedModelSerializer):
	"""
	Product Property Serializer
	"""    
	class Meta:
		model = ProductProperty

class RelatedProductSerializer(HyperlinkedModelSerializer):
	"""
	Product Serializer with nested properties to be included in the Product Group Represetation

	Product can be created without properites, then properties can be assigned later.
	"""
	properties = RelatedProductPropertySerializer(
		many=True,
		read_only=True,
	  	)
	class Meta:
		model = Product
		fields = ["url", "product_variation", "goss_price", "tax", "stock", "properties"]

class ProductSerializer(HyperlinkedModelSerializer):
	"""
	Product Serializer with nested properties.

	Product can be created without properites, then properties can be assigned later.
	"""
	product_group_name = serializers.StringRelatedField(source = "product_group", read_only=True)
	properties = RelatedProductPropertySerializer(
		many=True,
		read_only=True,
	  	)
	class Meta:
		model = Product

class ProductGroupSerializer(HyperlinkedModelSerializer):
	"""
	Product Group Serializer with nested products.

	ProductGroup can't be created without the nested products.
	"""
	products = RelatedProductSerializer(
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

