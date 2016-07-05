import json

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductGroup, Product

class ProductGroupTests(APITestCase):
	def setUp(self):
		prodcutgroup = ProductGroup(name="test product group")
		prodcutgroup.save()
		product = Product(product_variation="regular", goss_price="120.00", tax = "0.1200", stock=10, product_group = prodcutgroup)
		product.save()
		self.product = product

	def test_cant_create_productgroup_without_basic_data(self):
		"""
		Ensure we can't create a product group without the basic data (at least with one related product)
		"""
		url = reverse('productgroup-list')
		data = {'name': 'test product group'}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(ProductGroup.objects.count(), 1) #only one record should have been created in the setup

	def test_response_header_contain_etag_field (self):
		"""
		Ensure that the response contains ETAG header required for caching
		"""
		url = reverse('productgroup-list')
		response = self.client.get(url, format='json')
		self.assertTrue("ETAG" in response)
		self.assertTrue(response['ETAG'].strip() != '')


	def test_second_retrieval_issue_304_Not_Modified (self):
		"""
		Ensure that retrieving the same resource for the second time will issue HTTP_304_NOT_MODIFIED when If-None-Match
		header provided and contains the previously fetched `ETAG`
		"""
		url = reverse('productgroup-list')
		response1 = self.client.get(url, format='json')
		etag = response1["ETAG"]
		response2 = self.client.get(url, format='json', **{'If-None-Match':etag})
		self.assertEqual(response2.status_code, status.HTTP_304_NOT_MODIFIED)
		self.assertEqual(len(response2.content), 0)


class EndPointsTests(APITestCase):
	"""
	EndpointsTests presents the endpoints use test cases.
	"""
	def setUp(self):
		url = "/v1/productgroups/"
		data = {'name': 'Bag', 
				"products" : [
								{
									"product_variation": "regular", 
									"goss_price": "45.00", 
									"tax" : "0.1000", 
									"stock": 50
								}
							]
				}

		response = self.client.post(url, data, format='json')

		#create variation basic data
		parsed_json = json.loads(response.content)
		product_url = parsed_json['products'][0]['url']
		product_group_url = parsed_json['url']

		url = "/v1/products/"
		data = {
					"product_variation": "handbag", 
					"goss_price": "150.00", 
					"tax" : "0.1000", 
					"stock": 30,
					"product_group": product_group_url
				}
		handbag_response = self.client.post(url, data, format='json')

		#add variation characteristics
		url = "/v1/productproperties/"
		data = {'key': 'color', 
				'value' : '10 colors',
				'product' : product_url
				}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.content.find('10 colors') > -1)			

		url = "/v1/productproperties/"
		data = {'key': 'size', 
				'value' : 'from xs to xxl',
				'product' : product_url
				}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.content.find('from xs to xxl') > -1)

	def _create_regular_product (self):
		url = "/v1/productgroups/"
		data = {'name': 'Shirt', 
				"products" : [
								{
									"product_variation": "regular", 
									"goss_price": "120.00", 
									"tax" : "0.2000", 
									"stock": 20
								}
							]
				}
		return self.client.post(url, data, format='json')

	def test_create_regular_product(self):
		"""
		Ensure we can create a product group with product basic data "regular" product
		"""
		response = self._create_regular_product()
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.content.find('Shirt') > -1)

	def test_create_product_variation(self):
		"""
		Ensure we can create product variation and add characteristics to it
		"""
		#create regular product
		response = self._create_regular_product()

		#create variation basic data
		parsed_json = json.loads(response.content)
		product_group_url = parsed_json['url']

		url = "/v1/products/"
		data = {
					"product_variation": "Long Sleeve", 
					"goss_price": "200.00", 
					"tax" : "0.1500", 
					"stock": 30,
					"product_group": product_group_url
				}
		long_sleeve_response = self.client.post(url, data, format='json')
		long_sleeve_parsed_json = json.loads(response.content)
		long_sleeve_product_url = long_sleeve_parsed_json['products'][0]['url']
		self.assertEqual(long_sleeve_response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(long_sleeve_response.content.find("Long Sleeve") > -1)			

		#add variation characteristics
		url = "/v1/productproperties/"
		data = {'key': 'color', 
				'value' : '10 colors',
				'product' : long_sleeve_product_url
				}
		variation_prop1_response = self.client.post(url, data, format='json')
		self.assertEqual(variation_prop1_response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(variation_prop1_response.content.find('10 colors') > -1)			

		url = "/v1/productproperties/"
		data = {'key': 'size', 
				'value' : 'from xs to xxl',
				'product' : long_sleeve_product_url
				}
		variation_prop2_response = self.client.post(url, data, format='json')
		self.assertEqual(variation_prop2_response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(variation_prop2_response.content.find('from xs to xxl') > -1)		

	def test_update_product_group_name(self):
		"""
		Ensure we can change product group name
		"""

		#create the T-Shirt productgroup
		response = self._create_regular_product()
		parsed_json = json.loads(response.content)
		product_group_url = parsed_json['url']
		self.assertTrue(response.content.find('Shirt') > -1)


		#update the T-Shirt productgroup name to be Adidas T-Shirt
		url = product_group_url
		data = {'name': 'Adidas T-Shirt'}
		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.content.find('Adidas') > -1)

	def test_add_characteristics_to_product(self):
		"""
		Ensure we can add characteristics to regular product
		"""
		response = self._create_regular_product()
		parsed_json = json.loads(response.content)
		product_url = parsed_json['products'][0]['url']

		url = "/v1/productproperties/"
		data = {'key': 'color', 
				'value' : 'blue',
				'product' : product_url
				}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.content.find('blue') > -1)


	def test_delete_product(self):
		"""
		Ensure we can delete a product
		"""
		response = self._create_regular_product()
		parsed_json = json.loads(response.content)
		product_url = parsed_json['products'][0]['url']

		response = self.client.delete(product_url, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_list_product_groups_with_all_details(self):
		"""
		Ensure we can list avaliable product groups with all details
		"""
		response = self._create_regular_product()
		parsed_json = json.loads(response.content)
		product_url = parsed_json['products'][0]['url']

		url = "/v1/productgroups/"
		response = self.client.get(url, format='json')
		parsed_json = json.loads(response.content)
		count = parsed_json['count']
		self.assertTrue(count > 1)	
		self.assertTrue(response.content.find('Bag') > -1)
		self.assertTrue(response.content.find('handbag') > -1)
		self.assertTrue(response.content.find('color') > -1)
		self.assertTrue(response.content.find('size') > -1)


