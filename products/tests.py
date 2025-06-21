from django.test import TestCase
from django.urls import reverse
from products.models import Product, Category

# Create your tests here.

class ProductListViewTests(TestCase):

    def setUp(self):
        category = Category.objects.create(name='Test Category')
        Product.objects.create(
            name='Test Product',
            price=9.99,
            stock=10,
            category=category
        )

    def test_product_list_status_code(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_list_uses_correct_template(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_product_list_contains_correct_html(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '9.99')
        self.assertContains(response, '10')
        self.assertContains(response, 'Test Category')

    def test_product_name_in_response(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertContains(response, 'Test Product')

    def test_product_list_pagination(self):
        category, _ = Category.objects.get_or_create(name='Test Category')
        for i in range(20):
            Product.objects.create(
                name=f'Test Product {i}',
                price=9.99 + i,
                stock=10 + i,
                category=category
            )

        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_paginated', response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertLessEqual(len(response.context['products']), 8)
        self.assertContains(response, 'page=2')
        self.assertIn('pagination', response.content.decode())



