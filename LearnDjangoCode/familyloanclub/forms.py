# familyloanclub/forms.py

from django import forms
from .models import AccessRequest, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.core.validators import RegexValidator
import django_jalali.forms as jforms
from django_jalali.forms import jDateField


# فرم ثبت درخواست دسترسی
numeric_validator = RegexValidator(r'^\d+$', 'لطفاً فقط عدد وارد کنید.')


class AccessRequestForm(forms.ModelForm):
    phone_number = forms.CharField(
        label='شماره همراه شما',
        validators=[numeric_validator],
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً: 09123456789'})
    )
    referrer_phone = forms.CharField(
        label='شماره همراه معرف',
        validators=[numeric_validator],
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً: 09123456789'})
    )

    class Meta:
        model = AccessRequest
        fields = ['phone_number', 'referrer_phone']


# فرم تأیید کد دسترسی


class AccessCodeVerificationForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره همراه شما',
        validators=[numeric_validator],
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً: 09123456789'})
    )
    access_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(
            attrs={'placeholder': 'کد دسترسی', 'class': 'form-control'})
    )


class CompleteProfileForm(forms.Form):
    national_code = forms.CharField(
        label="کد ملی",
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        label="نام کاربری",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    birth_date = jDateField(
        label="تاریخ تولد (شمسی)",
        input_formats=['%Y/%m/%d', '%Y-%m-%d'],
        error_messages={
            'invalid': 'تاریخ را به‌درستی وارد کنید. مثلاً: ۱۴۰۰/۰۱/۰۱ یا ۱۴۰۰-۰۱-۰۱'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'مثلاً: ۱۴۰۰/۰۱/۰۱'
        })
    )


class AdminUserCreationForm(forms.Form):
    username = forms.CharField(label="نام کاربری (شماره همراه)", max_length=11,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label="نام کامل", max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    national_code = forms.CharField(label="کد ملی", max_length=10,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(
        label='شماره همراه شما',
        validators=[numeric_validator],
        widget=forms.TextInput(attrs={'placeholder': 'مثلاً: 09123456789'})
    )
    birth_date = jforms.jDateField(
        label="تاریخ تولد (روز/ماه/سال)",
        widget=jforms.jDateInput(attrs={'class': 'form-control'})
    )
    referrer_phone = forms.CharField(
        label='شماره همراه معرف (اختیاری)',
        validators=[numeric_validator],
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'مثلاً: 09123456789', 'class': 'form-control'})
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'birth_date',]


class PersianPasswordChangeForm(DjangoPasswordChangeForm):
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='''
            <ul class="text-danger">
                <li>رمز عبور نباید مشابه اطلاعات شخصی شما باشد.</li>
                <li>رمز عبور باید حداقل ۸ کاراکتر داشته باشد.</li>
                <li>رمز عبور نباید یک رمز رایج باشد.</li>
                <li>رمز عبور نباید فقط شامل اعداد باشد.</li>
            </ul>
        '''
    )
    new_password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='لطفاً رمز عبور جدید را دوباره وارد کنید.'
    )
