from django_tables2 import tables, TemplateColumn

from workingtime.models import EmployeeTable, Employee, CustomUserTable


# class EmploeeTable(tables.Table):
#     table_class = EmployeeTable
#     queryset = Employee.objects.all()
#     template_name = "Employee_list.html"
#     # delete = tables.TemplateColumn(template_name='main/delete_template.html', orderable=False)
#     acciones = TemplateColumn(
#         template_code='<a href="{% url "workingtime:employee_delete" record.id %}" class="btn btn-success">Ver</a>')
#
#     class Meta:
#         model = Employee
#         exclude = (
#             'engaged',
#         )


# class CustoUserTable(tables.Table):
#     table_class = CustomUserTable
#     queryset = Employee.objects.all()
#     template_name = "workingtime/customuser_list.html"
#     # delete = tables.TemplateColumn(template_name='main/delete_template.html', orderable=False)
#     # acciones = TemplateColumn(
#     #     template_code='<a href="{% url "workingtime:employee_delete" record.id %}" class="btn btn-success">Ver</a>')
#
#     class Meta:
#         model = Employee
#         exclude = (
#             'engaged',
#         )
