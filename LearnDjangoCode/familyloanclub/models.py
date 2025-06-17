from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


class AccessRequest(models.Model):
    phone_number = models.CharField(max_length=11)
    referrer_phone = models.CharField(max_length=11)
    access_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} (Verified: {self.is_verified})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_code = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=11)
    birth_date = jmodels.jDateField(
        verbose_name="تاریخ تولد (شمسی)", blank=True, null=True)
    referrer_phone = models.CharField(max_length=11, blank=True, null=True)
    referrer_name = models.CharField(max_length=150, blank=True, null=True)

    @property
    def referrer_name(self):
        try:
            ref_profile = Profile.objects.get(
                mobile_number=self.referrer_phone)
            return ref_profile.user.get_full_name() or ref_profile.user.username
        except Profile.DoesNotExist:
            return "نامشخص"

    def __str__(self):
        return self.user.get_full_name() or self.user.username
