from django import forms
from django.contrib.auth.forms import AuthenticationForm
from pip._internal.utils._jaraco_text import _

from workingtime.models import Employee, Timesheet


class MyAuthForm(AuthenticationForm):
    # Сейчас из темплейта сообщения
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = '__all__'