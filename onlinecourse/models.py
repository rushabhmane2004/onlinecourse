from django.db import models
from django.conf import settings
from django.utils.timezone import now

# 1. Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

# 2. Learner model
class Learner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20, choices=[('student', 'Student'), ('developer', 'Developer'), ('data_scientist', 'Data Scientist')], default='student')
    social_link = models.URLField(max_length=200)

# 3. Course model (Must be before Question)
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=500)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')

# 4. Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

# 5. Enrollment model
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [(AUDIT, 'Audit'), (HONOR, 'Honor')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

# 6. Question model
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    grade = models.IntegerField(default=5)

    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        return False

# 7. Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

# 8. Submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)