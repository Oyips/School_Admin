from django.contrib import admin
from .models import School, Class, Student, Attendance, Grade

admin.site.register(School)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Grade)