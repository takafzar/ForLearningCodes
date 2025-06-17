# familyloanclub/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views, update_session_auth_hash
from .forms import AccessRequestForm, AccessCodeVerificationForm, ProfileForm, AdminUserCreationForm, PersianPasswordChangeForm, CompleteProfileForm
from .models import AccessRequest, Profile
import random


def home(request):
    return render(request, 'familyloanclub/home.html')


def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(
                request, f"{user.get_full_name() or user.username}، خوش آمدید به باشگاه!")
            return redirect('home')
        else:
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                messages.error(
                    request, "نام کاربری یافت نشد! اگر ثبت‌نام نکرده‌اید، <a href='/request-access/'>عضویت</a> را انجام دهید.")
            else:
                messages.error(
                    request, "رمز عبور نادرست! <a href='#'>بازیابی رمز عبور</a>")
    else:
        form = AuthenticationForm()
    return render(request, 'familyloanclub/login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    messages.success(
        request, "شما با موفقیت از حساب خود خارج شدید. لطفاً دوباره وارد شوید.")
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    # اگه کاربر mode=edit زده، فرم ویرایش نمایش داده میشه
    mode = request.GET.get('mode', 'view')

    if mode == 'edit':
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            password_form = PersianPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "اطلاعات پروفایل با موفقیت به‌روزرسانی شد.")
                return redirect('profile')
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "رمز عبور با موفقیت تغییر یافت.")
                return redirect('profile')
        else:
            form = ProfileForm(instance=profile)
            password_form = PersianPasswordChangeForm(user)
        context = {
            'mode': 'edit',
            'profile': profile,
            'form': form,
            'password_form': password_form
        }
    else:
        # نمایش فقط نمایه
        context = {
            'mode': 'view',
            'profile': profile
        }

    return render(request, 'familyloanclub/profile.html', context)


def request_access_view(request):
    if request.method == 'POST':
        form = AccessRequestForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            ref_phone = form.cleaned_data['referrer_phone']
            ref_exists = Profile.objects.filter(
                mobile_number=ref_phone).exists()
            if not ref_exists:
                messages.error(
                    request, "شماره‌ی همراه معرف یافت نشد! لطفاً شماره‌ی معرف را بررسی کنید.")
            else:
                existing_request = AccessRequest.objects.filter(
                    phone_number=phone).first()
                if existing_request:
                    if existing_request.is_verified:
                        messages.info(
                            request, "درخواست شما قبلاً تأیید شده است. لطفاً کد دسترسی را وارد کنید.")
                        return redirect('verify_access_code')
                    else:
                        messages.info(
                            request, "درخواست عضویت شما در انتظار تأیید مدیر است.")
                else:
                    code = str(random.randint(100000, 999999))
                    AccessRequest.objects.create(
                        phone_number=phone,
                        referrer_phone=ref_phone,
                        access_code=code,
                        is_verified=False
                    )
                    messages.success(
                        request, "درخواست عضویت شما ثبت شد. لطفاً منتظر تأیید مدیر باشید.")
    else:
        form = AccessRequestForm()
    return render(request, 'familyloanclub/request_access.html', {'form': form})


def verify_access_code_view(request):
    if request.method == 'POST':
        form = AccessCodeVerificationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            code = form.cleaned_data['access_code']
            try:
                access_request = AccessRequest.objects.get(
                    phone_number=phone, access_code=code, is_verified=True)
                request.session['phone_number'] = phone
                messages.success(
                    request, "کد دسترسی تأیید شد. لطفاً مشخصات خود را تکمیل کنید.")
                return redirect('complete_profile')
            except AccessRequest.DoesNotExist:
                messages.error(
                    request, "کد وارد شده معتبر نیست یا هنوز تأیید نشده است.")
    else:
        form = AccessCodeVerificationForm()
    return render(request, 'familyloanclub/verify_access_code.html', {'form': form})


def complete_profile_view(request):
    phone_number = request.session.get('phone_number')
    if not phone_number:
        messages.error(
            request, "شماره همراه پیدا نشد. لطفاً دوباره تلاش کنید.")
        return redirect('verify_access_code')

    try:
        access_request = AccessRequest.objects.get(
            phone_number=phone_number, is_verified=True)
    except AccessRequest.DoesNotExist:
        messages.error(request, "کد دسترسی نامعتبر است.")
        return redirect('verify_access_code')

    referrer_phone = access_request.referrer_phone

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            national_code = form.cleaned_data['national_code']
            birth_date = form.cleaned_data['birth_date']

            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "این نام کاربری قبلاً استفاده شده است. لطفاً نام دیگری انتخاب کنید.")
                return redirect('complete_profile')

            user = User.objects.create_user(
                username=username, password=password)
            profile = Profile.objects.create(
                user=user,
                national_code=national_code,
                mobile_number=phone_number,
                birth_date=birth_date,
                referrer_phone=referrer_phone
            )
            messages.success(request, "ثبت‌نام شما با موفقیت انجام شد.")
            del request.session['phone_number']  # پاکسازی session
            return redirect('login')
    else:
        form = CompleteProfileForm()

    context = {
        'form': form,
        'phone_number': phone_number,
        'referrer_phone': referrer_phone
    }
    return render(request, 'familyloanclub/complete_profile.html', context)


@staff_member_required
def manage_access_requests(request):
    requests = AccessRequest.objects.all().order_by('-created_at')
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        access_request = AccessRequest.objects.get(id=request_id)
        if action == 'approve':
            access_request.is_verified = True
            access_request.save()
            messages.success(
                request, f"درخواست {access_request.phone_number} تأیید شد.")
        elif action == 'reject':
            access_request.delete()
            messages.info(
                request, f"درخواست {access_request.phone_number} حذف شد.")
        return redirect('manage_access_requests')
    return render(request, 'familyloanclub/manage_access_requests.html', {'requests': requests})


@staff_member_required
def admin_create_user_view(request):
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            full_name = form.cleaned_data['full_name']
            national_code = form.cleaned_data['national_code']
            mobile_number = form.cleaned_data['mobile_number']
            birth_date = form.cleaned_data['birth_date']  # تغییر به تاریخ شمسی
            # اینجا باید نام‌گذاری رو درست کنیم
            referrer_phone = form.cleaned_data['referrer_name']

            # اصلاح: referrer_name باید به referrer_phone تغییر نام بده
            referrer_name = ''
            if referrer_phone:
                try:
                    ref_profile = Profile.objects.get(
                        mobile_number=referrer_phone)
                    referrer_name = ref_profile.user.get_full_name() or ref_profile.user.username
                except Profile.DoesNotExist:
                    # فقط مدیر اجازه داره بدون معرف ادامه بده
                    messages.warning(
                        request, "شماره معرف یافت نشد. بدون معرف ثبت می‌شود.")
                    referrer_phone = ''
                    referrer_name = ''

            # چک تکراری بودن کاربر
            if User.objects.filter(username=username).exists():
                messages.error(
                    request, "کاربری با این شماره همراه قبلاً ثبت شده است.")
            else:
                user = User.objects.create_user(
                    username=username, password=password)
                user.first_name = full_name
                user.save()
                Profile.objects.create(
                    user=user,
                    national_code=national_code,
                    mobile_number=mobile_number,
                    birth_date=birth_date,
                    referrer_phone=referrer_phone,
                    referrer_name=referrer_name
                )
                messages.success(request, "کاربر جدید با موفقیت ثبت شد.")
                return redirect('admin_create_user')
    else:
        form = AdminUserCreationForm()
    return render(request, 'familyloanclub/admin_create_user.html', {'form': form})
