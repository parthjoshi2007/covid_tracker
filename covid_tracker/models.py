from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CovidAppUser(User):
    phone_number = models.CharField(max_length=10, unique=True)
    pincode = models.CharField(max_length=6)


