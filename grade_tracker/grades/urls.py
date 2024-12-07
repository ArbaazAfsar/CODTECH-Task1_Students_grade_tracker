from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/<int:student_id>/', views.student_report, name='student_report'),
    path('add-grade/', views.add_grade, name='add_grade'),
]
