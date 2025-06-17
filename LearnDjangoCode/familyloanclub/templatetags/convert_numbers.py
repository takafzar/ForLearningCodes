from django import template

register = template.Library()


def convert_to_persian(value):
    en_to_fa = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return str(value).translate(en_to_fa)


register.filter('persian', convert_to_persian)
