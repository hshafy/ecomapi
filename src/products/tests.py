from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from products.models import ProductGroup

class ProductGroupTests(APITestCase):
    def test_cant_create_productgroup_without_basic_data(self):
        """
        Ensure we can't create a product group without the basic data (at least with one related product)
        """
        url = reverse('productgroup-list')
        data = {'name': 'test product group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ProductGroup.objects.count(), 0)
