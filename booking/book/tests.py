from django.test import TestCase
from django.urls import reverse
from .models import Client, Service, ServiceType
from django.contrib.auth.models import User
from book.models import Client, Customer
from datetime import datetime, timedelta
from book.forms import DashboardAppointmentForm
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from book.models import Client, Customer, Category, Service, ServiceType
from book.forms import DashboardAppointmentForm, ServiceSearchForm
from datetime import time

# ... (other test classes you already have, like ClientServiceTest and LoginAndDashboardTest)

from datetime import time

class ClientServiceTest(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test client, service, and service type
        self.client_obj = Client.objects.create(
            user=self.user,
            business_name="Test Business",
            working_hours_start=time(hour=9),  # Provide a value for working_hours_start
            working_hours_end=time(hour=17),   # Provide a value for working_hours_end
            working_days="123",                # Provide a value for working_days (Mon, Tues, Wed)
        )
        self.service = Service.objects.create(client=self.client_obj, name="Test Service")
        self.service_type = ServiceType.objects.create(service=self.service, name="Test Service Type", price=100, description="Test Description", duration=60)


    def test_service_type_list(self):
        # Get the service type list page
        response = self.client.get(reverse('book:service_type_list', args=[self.client_obj.user.username]))

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the service type is displayed on the page
        self.assertContains(response, "Test Service Type")
        self.assertContains(response, "100")
        self.assertContains(response, "Test Description")
        self.assertContains(response, "60")

