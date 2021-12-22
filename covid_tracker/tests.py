from django.urls import reverse
from rest_framework.test import APITestCase


# Create your tests here.
from covid_tracker.models import CovidAppUser, CovidResult


class RegisterUserTestCase(APITestCase):
    def test_user_registered(self):
        user = {
            "first_name": "A",
            "last_name": "B",
            "phone_number": "9999999999",
            "pincode": "111111"
        }
        response = self.client.post(reverse('register-user'), user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', response.data)

    def test_admin_registered(self):
        user = {
            "first_name": "A",
            "last_name": "B",
            "phone_number": "9999999999",
            "pincode": "111111"
        }
        response = self.client.post(reverse('register-admin'), user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', response.data)
        user = CovidAppUser.objects.get(pk=response.data['user_id'])
        self.assertTrue(user.is_staff)


class SelfAssessmentTestCase(APITestCase):
    def test_95pct_risk(self):
        data = {
            'symptoms': ['fever', 'cough', 'headache'],
            'contact_with_covid_patient': True,
            'travel_history': True
        }
        response = self.client.post(reverse('self-assessment'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['risk_percentage'], 95)

    def test_75pct_risk(self):
        data = {
            'symptoms': ['fever', 'cough'],
            'contact_with_covid_patient': True,
            'travel_history': False
        }
        response = self.client.post(reverse('self-assessment'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['risk_percentage'], 75)

    def test_50pct_risk(self):
        data = {
            'symptoms': ['fever'],
            'contact_with_covid_patient': True,
            'travel_history': False
        }
        response = self.client.post(reverse('self-assessment'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['risk_percentage'], 50)

    def test_5pct_risk(self):
        data = {
            'symptoms': [],
            'contact_with_covid_patient': False,
            'travel_history': False
        }
        response = self.client.post(reverse('self-assessment'), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['risk_percentage'], 5)


class UpdateCovidStatusTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = {
            "first_name": "A",
            "last_name": "B",
            "phone_number": "9999999999",
            "pincode": "111111"
        }
        self.user_response = self.client.post(reverse('register-user'), self.user, format='json')
        self.admin = {
            "first_name": "A",
            "last_name": "B",
            "phone_number": "9999999998",
            "pincode": "111111",
        }
        self.admin_response = self.client.post(reverse('register-admin'), self.admin, format='json')

    def test_covid_status_updated(self):
        data = {
            'user_id': self.user_response.data['user_id'],
            'admin_id': self.admin_response.data['user_id'],
            'result': 'positive'
        }
        response = self.client.post(reverse('update-covid-status'), data)
        self.assertEqual(response.status_code, 200)
        user = CovidAppUser.objects.get(pk=data['user_id'])
        self.assertEqual(user.covidresult.result, CovidResult.POSITIVE)
