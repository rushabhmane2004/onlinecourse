from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# Create your views here.

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

# --- TASK 5 FUNCTIONS START HERE ---

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Get the selected choice ids from the POST request
        selected_ids = request.POST.getlist('choice')
        
        # Create a submission object
        # Note: This assumes the user is logged in and enrolled
        learner = request.user.learner
        enrollment = Enrollment.objects.get(learner=learner, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Add the selected choices to the submission
        for choice_id in selected_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        # Redirect to the result page
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    context['course'] = course
    context['submission'] = submission
    context['grade'] = 0
    
    # Calculate the grade by checking each question
    for question in course.question_set.all():
        # Get IDs of choices selected by the user for THIS specific question
        selected_ids = submission.choices.filter(question=question).values_list('id', flat=True)
        # Check if the selection for this question is correct
        if question.is_get_score(selected_ids):
            context['grade'] += question.grade
            
    return render(request, 'onlinecourse/exam_result.html', context)