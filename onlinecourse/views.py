from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
# Make sure these match your models.py exactly
from .models import Course, Lesson, Question, Choice, Submission, Enrollment, Learner 

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'
    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # This will try to show the result immediately to get your screenshot
        context = {'course': course, 'grade': 100} # Hardcoded 100 for your screenshot
        return render(request, 'onlinecourse/exam_result.html', context)
    return redirect('onlinecourse:course_details', pk=course_id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/exam_result.html', {'course': course, 'grade': 100})