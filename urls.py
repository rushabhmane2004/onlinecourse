from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Path for the course list (Home page)
    path('', views.CourseListView.as_view(), name='index'),
    
    # Path for course details
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    
    # --- TASK 6 PATHS START HERE ---
    
    # Path to submit the exam
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Path to show the exam result
    path('<int:course_id>/submission/<int:submission_id>/show_exam_result/', 
         views.show_exam_result, name='show_exam_result'),
]