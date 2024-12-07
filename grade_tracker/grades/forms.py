# forms.py
from django import forms
from .models import Grade,Subject
from django.forms import ModelForm

class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['subject', 'grade']

    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject")
    grade = forms.FloatField(
    widget=forms.NumberInput(attrs={'placeholder': 'Enter Grade'}),
    min_value=0, max_value=100,  # Ensuring the grade is within 0-100
    error_messages={
        'min_value': 'Grade must be at least 0.',
        'max_value': 'Grade cannot exceed 100.',
    }
    )
