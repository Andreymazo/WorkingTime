from django.db.models.signals import post_save
from django.dispatch import receiver

from workingtime.models import Timesheet, WorkTime


## Вместо сигнала в модели Timesheet все создает функция save
@receiver(post_save, sender=Timesheet)
def post_save_timesheet(instance, **kwargs):
    ww = WorkTime.objects.all().last()
    w = instance
    # print(w.worktime.status_work_wt)
    # print('timesheet updated, w.timesheet.status_work', w.__dict__)

    # ww.status_work_wt=w.status_work
    # ww.save()
