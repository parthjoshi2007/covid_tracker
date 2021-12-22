from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView

from covid_tracker.models import CovidAppUser, CovidResult


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


class UpdateCovidResultView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        admin_id = request.data['admin_id']
        admin_user = CovidAppUser.objects.get(pk=admin_id)
        if not admin_user.is_staff:
            return Response({'error': 'user is not admin', 'code': 'staff_user_required'}, status=400)
        result = CovidResult.objects.update_or_create(
            user_id=request.data['user_id'],
            defaults={'result': request.data['result']}
        )
        return Response({'updated': True})


class GetZoneInfoView(APIView):
    def get(self, request, *args, **kwargs):
        pincode = request.data['pincode']
        num_cases = (CovidAppUser.objects
                     .filter(pincode=pincode, covidresult__result=CovidResult.POSITIVE)
                     .count())
        if num_cases == 0:
            zone_type = 'green'
        elif num_cases < 5:
            zone_type = 'orange'
        else:
            zone_type = 'red'
        return Response({'num_cases': num_cases, 'zone_type': zone_type})
