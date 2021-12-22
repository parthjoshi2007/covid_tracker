from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CovidAppUser(User):
    phone_number = models.CharField(max_length=10, unique=True)
    pincode = models.CharField(max_length=6)


class CovidResult(models.Model):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    COVID_RESULT_CHOICES = (
        (POSITIVE, 'Positive'),
        (NEGATIVE, 'Negative'),
    )

    user = models.OneToOneField(CovidAppUser, on_delete=models.CASCADE)
    result = models.CharField(choices=COVID_RESULT_CHOICES, max_length=10)
