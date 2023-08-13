from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory, DateTimeField
from django.utils import timezone
from pip._internal.utils._jaraco_text import _

from workingtime.models import Employee, Timesheet, CustomUser, WorkTime


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


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


EmployeeFormSet = inlineformset_factory(CustomUser, Employee, form=CustomUserForm,
                                        formset=EmployeeForm,
                                        extra=1, max_num=20, can_delete=False)


class TimesheetForm(forms.ModelForm):
    datetime_start = DateTimeField(widget=DatePickerInput(format='%y-%m-%d'),
                         input_formats=('%y-%m-%d',),
                         required=False,
                         )
                         
    datetime_complete = DateTimeField(widget=DatePickerInput(format='%y-%m-%'),
                         input_formats=('%y-%m-%d',),
                         required=False,
                         )
    

    class Meta:
        model = Timesheet
        # fields = '__all__'
        fields = ['datetime_start', 'datetime_complete', 'status_work', 'employee']
        widgets = {
            "datetime_start": DatePickerInput(options={"format": "y-m-d", "value": timezone.now().strftime("%Y-%m-%d")}),
            "datetime_complete": DatePickerInput(options={"format": "y-m-d", "value": timezone.now().strftime("%Y-%m-%d")})
              }


class WorkTimeForm(forms.ModelForm):

    class Meta:
        model = WorkTime
        fields = '__all__'

