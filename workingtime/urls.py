from django.urls import path
from workingtime.apps import WorkingtimeConfig
from workingtime.views import CustomLoginView, EmploeeTableView,  \
    EmployeeDetail, EmployeeDelete, Timesheets

app_name = WorkingtimeConfig.name

urlpatterns = [

    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', EmploeeTableView.as_view(), name='home'),
    # path('timesheet/', timesheet, name='timesheet'),
    path('timesheet/', Timesheets.as_view(template_name="workingtime/timesheet.html"), name='timesheet'),

    path('employee/<int:pk>', EmployeeDetail.as_view(template_name="workingtime/employee_detail.html"), name='employee_detail'),
    # path('employee/<int:pk>', EmployeeDelete.as_view(), name='employee_delete'),

    # path('detail/<int:pk>/', RecordDetailView.as_view(), name='detail'),

]
