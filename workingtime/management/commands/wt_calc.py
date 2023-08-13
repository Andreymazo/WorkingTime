from django.core.management import BaseCommand
from django.db.models import Func, F, Value

from config.settings import BASE_DIR
from workingtime.models import WorkTime, Timesheet
#https://www.postgresql.org/docs/9.5/functions-matching.html
#queriset1 = Timesheet.objects.annotate(username_index=Func(F('username'), Value('(\d+)'), function='substring')).filter(status_work_wt__worktime=True) #'^[A-Z]{2}\d+$'
def work_time_calc():

    # qw = Timesheet.objects.annotate(status_work_wt__index=Func(F('status_work_wt'), Value('True'), function='SUM')).filter(worktime__status_work_wt=True)
    qw = Timesheet.objects.filter(worktime__status_work_wt=True)
    qw = Timesheet.objects.filter(worktime__work_safe_sheets=True)
    print(qw)
class Command(BaseCommand):
    def handle(self, *args, **options):
        work_time_calc()
        # print('BASE_DIR', BASE_DIR)