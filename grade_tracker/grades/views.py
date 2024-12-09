from django.shortcuts import render,redirect
from .forms import GradeForm,SearchForm
from .models import Grade, Student
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Student, Grade, Subject
from django.contrib import messages
from django.db.models import Q 
from django.db.models import Avg, Sum, Count




def home(request):
    user = request.user if request.user.is_authenticated else None  # Ensure `user` is always defined
    students = Student.objects.all()
    
    if request.user.is_authenticated:
        # Assuming you have a 'Student' model that relates to the user
        student = Student.objects.filter(user=user).first()  # Adjust as necessary
        grades = Grade.objects.filter(student=student) if student else []
    else:
        student = None
        grades = []

    return render(request, 'home.html', {
        'user': user,
        'student': student,
        'students': students,
        'grades': grades,
    })



def student_report(request, student_id):
    # Get the student object
    student = get_object_or_404(Student, id=student_id)
    
    # Fetch all grades related to the student
    grades = Grade.objects.filter(student=student)
    
    # Calculate total grades
    total_grades = round(sum(grade.grade for grade in grades), 2)
    
    # Assume the maximum possible grade per subject is 100
    total_possible_marks = len(grades) * 100
    
    # Calculate average grade
    average_grade = total_grades / len(grades) if grades else 0
    
    # Calculate percentage
    percentage = (total_grades / total_possible_marks) * 100 if total_possible_marks > 0 else 0
    
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
        'total_grades': total_grades,
        'total_possible_marks': total_possible_marks,
        'average': average_grade,
        'percentage': round(percentage, 2),
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



def grade_list(request):
    grades = Grade.objects.all()  # Initially fetch all grades
    form = SearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data['query']
        print(f"Query: {query}")  # Debugging line

        if query:
            # Apply OR logic with Q objects
            grades = grades.filter(
                Q(student__name__icontains=query) | 
                Q(subject__name__icontains=query) | 
                Q(grade__icontains=query)
            )

    print(grades.query)  # Print the SQL query to debug
    return render(request, 'grade_list.html', {'grades': grades, 'form': form})



def student_ranking_view(request):
    students = Student.objects.annotate(
        total_grades=Sum('grades__grade'),  # Calculate total grades
        total_subjects=Count('grades__grade')  # Count the total number of subjects
    ).order_by('-total_grades')  # Order by total grades in descending order

    # Calculate percentage and GPA for each student
    for student in students:
        # Assume each subject has a maximum grade of 100
        total_possible_marks = student.total_subjects * 100
        student.percentage = (
            (student.total_grades / total_possible_marks) * 100 if total_possible_marks > 0 else 0
        )
        
        # GPA logic based on average grades
        average_grade = student.total_grades / student.total_subjects if student.total_subjects > 0 else 0
        if average_grade >= 90:
            student.gpa = 4.0
        elif average_grade >= 80:
            student.gpa = 3.0
        elif average_grade >= 70:
            student.gpa = 2.0
        elif average_grade >= 60:
            student.gpa = 1.0
        else:
            student.gpa = 0.0

    context = {
        'students': students,
    }
    return render(request, 'student_ranking.html', context)




