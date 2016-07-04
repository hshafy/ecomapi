from rest_framework.viewsets import ModelViewSet

from products.serializers import ProductSerializer, ProductGroupSerializer, ProductPropertySerializer
from products.models import Product, ProductGroup, ProductProperty

class ProductGroupViewSet(ModelViewSet):
	"""
	This endpoint presents **products groups**.

	The `name` field presents product name

	You can perform GET, POST, PUT, PATCH, DELETE operations for list, detail, create, update, partial update and delete
	"""
	queryset = ProductGroup.objects.all()
	serializer_class = ProductGroupSerializer

class ProductViewSet(ModelViewSet):
	"""
	This endpoint presents **products**.

	The `gross_price` gross price is a number that may contain 2 decimal places i.e. 199.99
	The `tax` field should be a number between 0 and 1 with a maximum of 4 decimal places i.e 0.2575 that represents 25.75%
	The `stock` field represent the avaliable stock of the product and is an integer number
	The `product_group` field represent the product group resource url

	You can perform GET, POST, PUT, PATCH, DELETE operations for list, detail, create, update, partial update and delete
	"""
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class ProductPropertyViewSet(ModelViewSet):
	"""
	This endpoint presents **products properties**.

	The `key`, `value` fields presents products attributes in free text key value pair 

	You can perform GET, POST, PUT, PATCH, DELETE operations for list, detail, create, update, partial update and delete
	"""
	queryset = ProductProperty.objects.all()
	serializer_class = ProductPropertySerializer
