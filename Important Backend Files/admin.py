from django.contrib.admin import AdminSite
from django.contrib import admin
from Democritus.models import StudentList, Poll


class DemocritusAdmin(AdminSite):
    site_header = 'Democritus Administration'
    site_title = 'Democritus Admin'


admin_site = DemocritusAdmin(name='demoadmin')
admin_site.register(StudentList)
admin_site.register(Poll)

