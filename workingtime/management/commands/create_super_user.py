from django.core.management import BaseCommand

from workingtime.models import CustomUser


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            email='andreymazo@mail.ru',
            is_admin=True,
            # is_staff=True
        )
        user.set_password('qwert123asd')
        user.is_superuser = True
        user.save()
