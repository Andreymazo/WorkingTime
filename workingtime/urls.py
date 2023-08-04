from django.urls import path
from workingtime.apps import WorkingtimeConfig
from workingtime.formset import CustomuserCreateWithSubject
from workingtime.views import CustomLoginView, \
    EmployeeDetail, EmployeeDelete, Timesheets, EmploeeTable, TimesheetLst, EmployeeUpdate, EmployeeCreate, \
    EmploeeTableView, CustomUserLst

app_name = WorkingtimeConfig.name

urlpatterns = [

    path('', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', EmploeeTableView.as_view(), name='home'),
    path('timesheet_get_time/', TimesheetLst.as_view(), name='timesheet_lst'),
    path('timesheet/', Timesheets.as_view(template_name="workingtime/timesheet.html"), name='timesheet'),
    path('employee_lst/', EmploeeTable.as_view(template_name="workingtime/employee_list2.html"), name='employee_lst'),
    path('employee_create/', EmployeeCreate.as_view(template_name="workingtime/employee_form.html"), name='employee_create'),
    path('employee_detail/<int:pk>', EmployeeDetail.as_view(template_name="workingtime/employee_detail.html"), name='employee_detail'),
    path('employee_update/<int:pk>', EmployeeUpdate.as_view(template_name="workingtime/employee_form.html"), name='employee_update'),
    path('employee_delete/<int:pk>', EmployeeDelete.as_view(template_name='workingtime/employee_confirm_delete.html'), name='employee_delete'),

    path('customuser_lst/', CustomUserLst.as_view(), name='customuser_lst'),
    path('customuser_create/', CustomuserCreateWithSubject.as_view(), name='customuser_create'),
    # path('employee/<int:pk>', EmployeeDelete.as_view(), name='delete_item'),

    # path('detail/<int:pk>/', RecordDetailView.as_view(), name='detail'),

]
