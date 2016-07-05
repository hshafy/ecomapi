from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductGroup

class ProductGroupTests(APITestCase):
	def setUp(self):
		prodcutgroup = ProductGroup(name="test product group")
		prodcutgroup.save()

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
		header provided and contains the previously fetched ETAG
		"""
		url = reverse('productgroup-list')
		response1 = self.client.get(url, format='json')
		etag = response1["ETAG"]
		response2 = self.client.get(url, format='json', **{'If-None-Match':etag})
		self.assertEqual(response2.status_code, status.HTTP_304_NOT_MODIFIED)
		self.assertEqual(len(response2.content), 0)

