from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import School, Class, Student


@login_required
def dashboard(request):
    user = request.user

    if user.role == 'platform_admin':
        context = {
            'schools': School.objects.all(),
            'pending_schools': School.objects.filter(is_approved=False),
        }
        return render(request, 'school_app/dashboard_admin.html', context)

    if user.role == 'school_owner':
        context = {
            'school': user.school,
            'classes': Class.visible_to(user),
            'students': Student.visible_to(user),
        }
        return render(request, 'school_app/dashboard_owner.html', context)

    if user.role == 'teacher':
        context = {
            'classes': Class.visible_to(user),
            'students': Student.visible_to(user),
        }
        return render(request, 'school_app/dashboard_teacher.html', context)

    if user.role == 'student':
        context = {
            'profile': Student.visible_to(user).first(),
        }
        return render(request, 'school_app/dashboard_student.html', context)