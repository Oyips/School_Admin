from django.db import models
from django.conf import settings


class School(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                  null=True, related_name='owned_school')
    logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                 null=True, related_name='assigned_classes')

    def __str__(self):
        return f"{self.school.name} - {self.name}"

    @staticmethod
    def visible_to(user):
        if user.role == 'platform_admin':
            return Class.objects.all()
        if user.role == 'school_owner':
            return Class.objects.filter(school=user.school)
        if user.role == 'teacher':
            return Class.objects.filter(teacher=user)
        return Class.objects.none()


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def visible_to(user):
        if user.role == 'platform_admin':
            return Student.objects.all()
        if user.role == 'school_owner':
            return Student.objects.filter(school=user.school)
        if user.role == 'teacher':
            return Student.objects.filter(school_class__teacher=user)
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.none()


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.present else 'Absent'}"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    school_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"