from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from pip._internal.utils._jaraco_text import _

from workingtime.models import Employee, Timesheet, CustomUser


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


# class CreatePacketForm(forms.ModelForm):
#     """
#     CreatePacketForm class
#     """
#     class Meta:
#         model = Packet
#         exclude = ('customer', 'created_on', 'updated_on',
#                    'created_by', 'updated_by', 'remark', 'p_id'
#                    )
# ItemFormSet = inlineformset_factory(Packet, Item, form=CreatePacketForm,
#                                     formset=CreateItemForm,
#                                     extra=1, max_num=20, can_delete=False)


class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheet
        fields = '__all__'
