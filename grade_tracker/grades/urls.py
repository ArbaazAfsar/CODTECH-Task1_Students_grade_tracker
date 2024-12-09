from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/<int:student_id>/', views.student_report, name='student_report'),
    path('add-grade/', views.add_grade, name='add_grade'),
    path('grades/', views.grade_list, name='grade_list'),
    path('rankings/', views.student_ranking_view, name='student_rankings'),
]
