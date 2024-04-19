from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404


def subscribe(user):
    """
    Выдача прав пользователю после подписки
    """
    user_instance = get_object_or_404(get_user_model(), phone_number=user)
    permission = Permission.objects.get(codename='view_publication')
    if permission:
        user_instance.user_permissions.add(permission)
