from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from covid_tracker.models import CovidAppUser


class RegisterUserView(APIView):
    http_method_names = ['post']

    def make_username(self, name):
        return ' '.join(name.split()).replace(' ', '-') + get_random_string(5)

    def create_user(self, request_data):
        return CovidAppUser.objects.create_user(
            self.make_username(request_data['first_name']),
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            phone_number=request_data['phone_number'],
            pincode=request_data['pincode']
        )

    def post(self, request, *args, **kwargs):
        user = self.create_user(request.data)
        return Response({'user_id': user.pk})


class SelfAssessmentView(APIView):
    http_method_names = ['post']

    def assess_user_risk(self, request_data):
        del self
        symptoms = request_data['symptoms']
        travel_history = request_data['travel_history']
        contact_with_covid_patient = request_data['contact_with_covid_patient']
        if not symptoms and not travel_history and not contact_with_covid_patient:
            return 5
        elif len(symptoms) == 1 and (travel_history or contact_with_covid_patient):
            return 50
        elif len(symptoms) == 2 and (travel_history or contact_with_covid_patient):
            return 75
        elif len(symptoms) > 2 and (travel_history or contact_with_covid_patient):
            return 95
        else:
            # No symptoms but travel history or contact
            return 20

    def post(self, request, *args, **kwargs):
        return Response({'risk_percentage': self.assess_user_risk(request.data)})


class RegisterAdminUserView(RegisterUserView):
    http_method_names = ['post']

    def create_user(self, request_data):
        return CovidAppUser.objects.create_user(
            self.make_username(request_data['first_name']),
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            phone_number=request_data['phone_number'],
            pincode=request_data['pincode'],
            is_staff=True
        )
