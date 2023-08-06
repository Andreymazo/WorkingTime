from django.contrib import admin

from workingtime.models import Employee, CustomUser, Timesheet

admin.site.register(Employee)

admin.site.register(CustomUser)

admin.site.register(Timesheet)
