from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from movies.models import Movie
from .models import Order


class PurchaseRegionTaggingTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='bob', password='pass1234')
		img = SimpleUploadedFile('m.jpg', b'filecontent', content_type='image/jpeg')
		self.movie = Movie.objects.create(name='Test Movie', price=15, description='desc', image=img)

	def _put_movie_in_cart(self, qty=1):
		session = self.client.session
		session['cart'] = {str(self.movie.id): qty}
		session.save()

	def test_purchase_uses_session_region(self):
		self.client.login(username='bob', password='pass1234')
		# set preferred region in session
		session = self.client.session
		session['preferred_region_code'] = 'USA'
		session.save()
		# put movie into cart
		self._put_movie_in_cart(qty=2)
		# perform purchase
		resp = self.client.get(reverse('cart.purchase'))
		self.assertEqual(resp.status_code, 200)
		# verify last order has region_code set
		order = Order.objects.latest('id')
		self.assertEqual(order.region_code, 'USA')

	def test_purchase_query_param_overrides_session(self):
		self.client.login(username='bob', password='pass1234')
		# set different session region
		session = self.client.session
		session['preferred_region_code'] = 'USA'
		session.save()
		self._put_movie_in_cart(qty=1)
		# override via ?region=CAN
		resp = self.client.get(reverse('cart.purchase') + '?region=CAN')
		self.assertEqual(resp.status_code, 200)
		order = Order.objects.latest('id')
		self.assertEqual(order.region_code, 'CAN')
