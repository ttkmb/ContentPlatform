import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(phone_number=os.getenv('ADMIN_LOGIN_PHONE'), is_staff=True,
                                   is_superuser=True)
        user.set_password('admin')
        user.save()
