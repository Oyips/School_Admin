from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import School, Class, Student
from django.shortcuts import redirect
from .forms import ClassForm, StudentForm
from datetime import date
from .models import Attendance
from .forms import AttendanceDateForm
from .models import Grade
from .forms import GradeEntryForm


@login_required
def mark_attendance(request, class_id):
    school_class = Class.objects.get(id=class_id)

    # security check: this class must actually belong to this teacher
    if school_class.teacher != request.user:
        return redirect('dashboard')

    selected_date = request.GET.get('date', str(date.today()))
    students = Student.objects.filter(school_class=school_class)

    if request.method == 'POST':
        for student in students:
            present = request.POST.get(f'present_{student.id}') == 'on'
            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={'present': present, 'school_class': school_class, 'marked_by': request.user}
            )
        return redirect('dashboard')

    # for each student, check if there's already a record for this date (to pre-fill the checkbox)
    existing = {a.student_id: a.present for a in Attendance.objects.filter(
        school_class=school_class, date=selected_date)}

    student_rows = [
        {'student': s, 'present': existing.get(s.id, True)} for s in students
    ]

    context = {
        'school_class': school_class,
        'student_rows': student_rows,
        'selected_date': selected_date,
    }
    return render(request, 'school_app/mark_attendance.html', context)


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
      classes = Class.visible_to(user)
      attendance_summary = []
      for c in classes:
        total = Attendance.objects.filter(school_class=c).count()
        present = Attendance.objects.filter(school_class=c, present=True).count()
        rate = round((present / total) * 100, 1) if total else 0
        attendance_summary.append({'name': c.name, 'rate': rate})

      context = {
        'school': user.school,
        'classes': classes,
        'students': Student.visible_to(user),
        'attendance_summary': attendance_summary,
      }
      return render(request, 'school_app/dashboard_owner.html', context)
    if user.role == 'teacher':
        context = {
            'classes': Class.visible_to(user),
            'students': Student.visible_to(user),
        }
        return render(request, 'school_app/dashboard_teacher.html', context)

    if user.role == 'student':
      profile = Student.visible_to(user).first()
      context = {
        'profile': profile,
        'attendance_records': profile.attendance_records.order_by('-date')[:30] if profile else [],
        'grades': profile.grades.order_by('-date_recorded') if profile else [],
      }
      return render(request, 'school_app/dashboard_student.html', context)

  

@login_required
def create_class(request):
    if request.user.role != 'school_owner':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ClassForm(request.POST, school=request.user.school)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class.school = request.user.school
            new_class.save()
            return redirect('dashboard')
    else:
        form = ClassForm(school=request.user.school)

    return render(request, 'school_app/create_class.html', {'form': form})


@login_required
def add_student(request):
    if request.user.role != 'school_owner':
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, school=request.user.school)
        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.school = request.user.school
            new_student.save()
            return redirect('dashboard')
    else:
        form = StudentForm(school=request.user.school)

    return render(request, 'school_app/add_student.html', {'form': form})

  


@login_required
def enter_grades(request, class_id):
    school_class = Class.objects.get(id=class_id)

    if school_class.teacher != request.user:
        return redirect('dashboard')

    students = Student.objects.filter(school_class=school_class)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        grade_date = request.POST.get('date')
        for student in students:
            score = request.POST.get(f'score_{student.id}')
            if score:  # skip blanks — don't create a grade with no value
                Grade.objects.update_or_create(
                    student=student,
                    school_class=school_class,
                    subject=subject,
                    defaults={'score': score}
                )
        return redirect('dashboard')

    context = {
        'school_class': school_class,
        'students': students,
    }
    return render(request, 'school_app/enter_grades.html', context)

@login_required
def approve_school(request, school_id):
    if request.user.role != 'platform_admin':
        return redirect('dashboard')

    school = School.objects.get(id=school_id)
    school.is_approved = True
    school.save()
    return redirect('dashboard')