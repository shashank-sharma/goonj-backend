import datetime

from django.db import models

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from accounts.models import User, Donator


class DonatingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.CharField(max_length=280)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=20, decimal_places=12)
    longitude = models.DecimalField(max_digits=20, decimal_places=12)
    start_datetime = models.DateTimeField(auto_now_add=True)
    end_datetime = models.DateTimeField(blank=True)


class Donation(models.Model):
    donator = models.ForeignKey(Donator, on_delete=models.CASCADE)
    donating_session = models.OneToOneField(DonatingSession, on_delete=models.CASCADE)
    material = models.TextField(blank=True)
    received_by_volunteer = models.BooleanField(default=False)
    received_by_center = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    received_at_volunteer = models.DateTimeField(blank=True)
    received_at_center = models.DateTimeField(blank=True)

