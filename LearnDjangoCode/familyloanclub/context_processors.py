# familyloanclub/context_processors.py
def user_links(request):
    user = request.user
    links = []
    if user.is_authenticated:
        # بعداً URL پروفایل بساز
        links.append({'name': 'پروفایل من', 'url': 'profile'})
        # بعداً URL درخواست وام بساز
        links.append({'name': 'درخواست وام', 'url': '#'})
        if user.is_staff:
            links.append({'name': 'مدیریت درخواست‌ها',
                         'url': 'manage_access_requests'})
            links.append({'name': 'افزودن کاربر', 'url': 'admin_create_user'})
        links.append({'name': 'خروج', 'url': 'logout'})
    else:
        links.append({'name': 'ورود', 'url': 'login'})
        links.append({'name': 'عضویت', 'url': 'request_access'})
    return {'user_links': links}


def session_expiry_time(request):
    if request.user.is_authenticated:
        expiry = request.session.get_expiry_age()
        return {'session_expiry_time': expiry}
    return {}
