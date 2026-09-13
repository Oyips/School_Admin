from django import forms
from .models import Class, Student
from accounts.models import User


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'teacher']

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school:
            # only let the owner assign teachers who belong to their own school
            self.fields['teacher'].queryset = User.objects.filter(school=school, role='teacher')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'photo', 'school_class']

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        if school:
            # only let the owner assign students to classes within their own school
            self.fields['school_class'].queryset = Class.objects.filter(school=school)