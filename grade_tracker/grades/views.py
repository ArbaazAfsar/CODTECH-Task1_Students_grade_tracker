from django.shortcuts import render,redirect
from .forms import GradeForm
from .models import Grade, Student
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Grade, Subject
from django.contrib import messages




def home(request):
    students = Student.objects.all()
    return render(request, "home.html", {"students": students})


def student_report(request, student_id):
    # Get the student object
    student = get_object_or_404(Student, id=student_id)
    
    # Fetch all grades related to the student
    grades = Grade.objects.filter(student=student)
    
    # Calculate average grade
    total_grades = round(sum(grade.grade for grade in grades), 2)
    average_grade = total_grades / len(grades) if grades else 0
    
    # Determine letter grade
    if average_grade >= 90:
        letter_grade = 'A'
    elif average_grade >= 80:
        letter_grade = 'B'
    elif average_grade >= 70:
        letter_grade = 'C'
    elif average_grade >= 60:
        letter_grade = 'D'
    else:
        letter_grade = 'F'
    
    # Determine GPA
    if average_grade >= 90:
        gpa = 4.0
    elif average_grade >= 80:
        gpa = 3.0
    elif average_grade >= 70:
        gpa = 2.0
    elif average_grade >= 60:
        gpa = 1.0
    else:
        gpa = 0.0
    
    # Render the report page with the relevant data
    return render(request, 'student_report.html', {
        'student': student,
        'grades': grades,
        'average': average_grade,
        'letter_grade': letter_grade,
        'gpa': gpa
    })


@login_required
def add_grade(request):
    student = Student.objects.get(user=request.user)  # Get the student associated with the logged-in user

    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            grade = form.cleaned_data['grade']
            
            # Check if a grade already exists for this student and subject
            if Grade.objects.filter(student=student, subject=subject).exists():
                messages.error(request, "You have already added a grade for this subject.")
            else:
                # If no grade exists for this subject, save the new grade
                Grade.objects.create(student=student, subject=subject, grade=grade)
                messages.success(request, "Grade added successfully!")
            
            return redirect('add_grade')  # Redirect to refresh the page and show updated grades

    else:
        form = GradeForm()

    # Fetch existing grades of the student
    grades = Grade.objects.filter(student=student)

    return render(request, 'add_grade.html', {'form': form, 'grades': grades, 'student': student})

