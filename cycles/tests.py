# Create your tests here.
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Cycle

class CycleAPITestCase(APITestCase):
    def setUp(self):
        # This method is run before each test
        self.client = APIClient()
        self.cycle_data = {'name': 'Test Cycle', 'description': 'This is a test cycle'}
        self.cycle = Cycle.objects.create(name='Existing Cycle', description='Existing cycle description')

    def test_get_cycles(self):
        # Test GET request for list of cycles
        response = self.client.get(reverse('cycle-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if one cycle is returned

    def test_create_cycle(self):
        # Test POST request to create a new cycle
        response = self.client.post(reverse('cycle-list'), self.cycle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cycle.objects.count(), 2)  # Two cycles should exist now
        self.assertEqual(Cycle.objects.get(id=response.data['id']).name, 'Test Cycle')

    def test_get_single_cycle(self):
        # Test GET request for a single cycle
        response = self.client.get(reverse('cycle-detail', kwargs={'pk': self.cycle.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Cycle')
