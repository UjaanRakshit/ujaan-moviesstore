from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from movies.models import Movie
from cart.models import Order, Item


class RegionAggregationApiTests(TestCase):
	def setUp(self):
		self.client = Client()
		# Create sample user
		self.user = User.objects.create_user(username='alice', password='pass1234')
		# Create sample movies (use small dummy image bytes)
		img = SimpleUploadedFile('test.jpg', b'filecontent', content_type='image/jpeg')
		self.m1 = Movie.objects.create(name='Movie A', price=10, description='A', image=img)
		img2 = SimpleUploadedFile('test2.jpg', b'filecontent', content_type='image/jpeg')
		self.m2 = Movie.objects.create(name='Movie B', price=12, description='B', image=img2)

		# Create orders with region codes and items
		o1 = Order.objects.create(user=self.user, total=22, region_code='USA')
		Item.objects.create(order=o1, movie=self.m1, price=10, quantity=1)
		Item.objects.create(order=o1, movie=self.m2, price=12, quantity=1)

		o2 = Order.objects.create(user=self.user, total=20, region_code='USA')
		Item.objects.create(order=o2, movie=self.m1, price=10, quantity=2)

		o3 = Order.objects.create(user=self.user, total=12, region_code='CAN')
		Item.objects.create(order=o3, movie=self.m2, price=12, quantity=1)

	def test_region_popularity(self):
		resp = self.client.get(reverse('api.region_popularity'))
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		regions = data.get('regions', {})
		# USA: m1 qty 1+2=3, m2 qty 1 => total 4
		# CAN: m2 qty 1 => total 1
		self.assertEqual(regions.get('USA'), 4)
		self.assertEqual(regions.get('CAN'), 1)

	def test_region_top_movies(self):
		resp = self.client.get(reverse('api.region_top', kwargs={'region_code': 'USA'}))
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		top = data.get('top', [])
		# Expect Movie A with count 3 first
		self.assertTrue(len(top) >= 1)
		self.assertEqual(top[0]['title'], 'Movie A')
		self.assertEqual(top[0]['count'], 3)

	def test_set_region(self):
		resp = self.client.post(reverse('api.set_region'), data={"region_code": "USA"}, content_type='application/json')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(resp.json().get('success'))
