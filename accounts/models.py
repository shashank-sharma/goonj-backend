import datetime
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager, DonatorManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model to implement login with phone_number and password

    """
    email = models.EmailField(_('email address'), blank=True)
    phone_number = models.CharField(_('phone number'), max_length=10, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=8, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_worker = models.BooleanField(_('worker'), default=False)
    is_volunteer = models.BooleanField(_('volunteer'), default=False)
    is_online = models.BooleanField(_('online'), default=False)
    last_activity = models.DateTimeField(_('last activity'), default=datetime.date.today)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    otp = models.CharField(max_length=4, null=False, blank=False, default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def volunteer(self):
        return self.is_volunteer

    @property
    def admin(self):
        return self.is_admin


class GoonjCenter(models.Model):
    is_dropping_center = models.BooleanField(default=False)
    address = models.CharField(max_length=600)
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    start_time = models.TimeField(default='10:00')
    end_time = models.TimeField(default='17:00')


# TODO: Finalize Worker model
class Worker(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    goonj_center = models.OneToOneField(GoonjCenter, on_delete=models.CASCADE, null=True, blank=True)


# TODO: Finalize Volunteer model
class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    donating_session_active = models.BooleanField(default=False)
    goonj_center = models.OneToOneField(GoonjCenter, on_delete=models.CASCADE, null=True, blank=True)


class Donator(models.Model):
    objects = DonatorManager()

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=8)
    date_joined = models.DateTimeField(auto_now_add=True)
