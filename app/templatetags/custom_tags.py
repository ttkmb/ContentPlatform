from django import template

from app.models import Subscription

register = template.Library()


@register.simple_tag
def check_subscription(user):
    if user.is_authenticated:
        return Subscription.objects.filter(user=user).exists()
    else:
        return False
