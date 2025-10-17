from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Payment

class PaymentTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.com')
        self.payment = Payment.objects.create(
            user=self.user,
            amount=1000,
            payment_method="cash"
        )

    def test_payment_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('users:payment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)