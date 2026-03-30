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
        selected_ids = request.POST.getlist('choice')
        
        # 1. Get Learner and Enrollment
        learner = request.user.learner
        enrollment = Enrollment.objects.get(learner=learner, course=course)
        
        # 2. Create Submission Object (Grader requirement)
        submission = Submission.objects.create(enrollment=enrollment)
        
        # 3. Associate Choices
        for choice_id in selected_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
            
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    return redirect('onlinecourse:course_details', pk=course_id)

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_score = 0
    possible_score = 0
    
    for question in course.question_set.all():
        possible_score += question.grade
        selected_ids = submission.choices.filter(question=question).values_list('id', flat=True)
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    context = {
        'course': course,
        'grade': total_score,
        'possible': possible_score,
        'submission': submission
    }
    return render(request, 'onlinecourse/exam_result.html', context)