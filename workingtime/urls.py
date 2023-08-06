from django.urls import path
from workingtime.apps import WorkingtimeConfig
from workingtime.formset import CustomuserCreateWithEmployee
from workingtime.views import CustomLoginView, \
    EmployeeDetail, EmployeeDelete, Timesheets, EmploeeTable, TimesheetLst, EmployeeUpdate, EmployeeCreate, \
    EmploeeTableView, CustomUserLst

app_name = WorkingtimeConfig.name

urlpatterns = [

    path('', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('employee_self/', EmploeeTableView.as_view(), name='employee_self'),
    path('timesheet_get_self_time/', TimesheetLst.as_view(), name='timesheet_lst_self_time'),
    path('timesheet/', Timesheets.as_view(template_name="workingtime/timesheet.html"), name='timesheet'),
    path('employee_lst/', EmploeeTable.as_view(template_name="workingtime/employee_list2.html"), name='employee_lst'),
    path('customuser_create/', CustomuserCreateWithEmployee.as_view(), name='customuser_create'),
    # path('employee_create/', EmployeeCreate.as_view(template_name="workingtime/employee_form.html"), name='employee_create'),
    path('employee_detail/<int:pk>', EmployeeDetail.as_view(template_name="workingtime/employee_detail.html"), name='employee_detail'),
    # По аналогии с криейт надо заменить employee_update/ на customuser_update/ с использованеим formset, хотя и сейчас можно менять все кроме емэйла
    path('employee_update/<int:pk>', EmployeeUpdate.as_view(template_name="workingtime/employee_form.html"), name='employee_update'),
    path('employee_delete/<int:pk>', EmployeeDelete.as_view(template_name='workingtime/employee_confirm_delete.html'), name='employee_delete'),
    # На темлейте customuser_list.html не редактировал еще ничего
    path('customuser_lst/', CustomUserLst.as_view(), name='customuser_lst'),

]
