from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    cohort = models.ForeignKey('Cohort', on_delete=models.SET_NULL, null=True, blank=True, related_name='learners')

    def __str__(self):
        return self.get_full_name() or self.username


class Cohort(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Week(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name='weeks')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='default', blank=True)

    class Meta:
        ordering = ['number']
        unique_together = ['cohort', 'number']

    def __str__(self):
        return f"Week {self.number}: {self.title}"

    def is_unlocked_for(self, learner):
        if self.number == 1:
            return True
        previous_weeks = Week.objects.filter(cohort=self.cohort, number__lt=self.number)
        total_previous = previous_weeks.count()
        if total_previous == 0:
            return False
        passed_count = WeeklyProgress.objects.filter(
            learner=learner, week__in=previous_weeks, status='passed'
        ).count()
        return passed_count == total_previous

    def is_next_to_attempt(self, learner):
        if not self.is_unlocked_for(learner):
            return False
        return not WeeklyProgress.objects.filter(
            learner=learner, week=self, status='passed'
        ).exists()


class Topic(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='default', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ReferenceMaterial(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='default', blank=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} — {self.title}"


class Tool(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='tools')
    name = models.CharField(max_length=200)
    developer = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = CKEditor5Field('Description', config_name='default', blank=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ToolFeature(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    purpose = CKEditor5Field('Purpose', config_name='default')
    how_to_use = CKEditor5Field('How to use', config_name='default')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.tool.name} — {self.title}"


class Assignment(models.Model):
    SUBMISSION_TYPES = [
        ('link', 'External Link'),
        ('text', 'Written Response'),
        ('both', 'Link + Written Notes'),
    ]
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='assignments')
    tool = models.ForeignKey(Tool, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    title = models.CharField(max_length=200)
    description = CKEditor5Field('Description', config_name='default', blank=True)
    prompt = CKEditor5Field('Prompt', config_name='default')
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPES, default='link')
    is_open_ended = models.BooleanField(default=True)

    class Meta:
        ordering = ['week__number', 'id']

    def __str__(self):
        return f"{self.week} — {self.title}"


class RubricCriterion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    max_score = models.PositiveIntegerField(default=20)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.assignment.title} — {self.name}"


class PeerPairing(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='pairings', null=True, blank=True)
    learner_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pairings_as_a', null=True, blank=True)
    learner_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pairings_as_b', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='submissions_to_review',
        help_text='The chosen peer reviewer for this submission.'
    )
    link = models.URLField(blank=True)
    text_content = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ['assignment', 'learner']
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.learner} — {self.assignment.title}"

    @property
    def review(self):
        return self.reviews.filter(is_valid=True).first()

    @property
    def percentage(self):
        review = self.review
        if review and self.assignment.criteria.exists():
            max_total = sum(c.max_score for c in self.assignment.criteria.all())
            if max_total > 0:
                return round((review.total_score / max_total) * 100, 2)
        return None


class ReviewRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='review_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_requests_sent')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_requests_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['submission'], name='one_request_per_submission')
        ]

    def __str__(self):
        return f"{self.requester} → {self.reviewer} ({self.status})"


class Review(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    comment = models.TextField()
    criterion_scores = models.JSONField(default=dict)
    total_score = models.FloatField(default=0)
    is_valid = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        min_len = 20
        self.is_valid = bool(self.comment and len(self.comment.strip()) >= min_len)
        if self.criterion_scores:
            self.total_score = sum(float(v) for v in self.criterion_scores.values())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review of {self.submission} by {self.reviewer}"


class WeeklyProgress(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    ]
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_progress')
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='progress_records')
    average_score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['learner', 'week']

    def __str__(self):
        return f"{self.learner} — Week {self.week.number} — {self.status}"

    def compute(self):
        from django.conf import settings
        assignments = self.week.assignments.all()
        percentages = []
        for a in assignments:
            sub = Submission.objects.filter(assignment=a, learner=self.learner).first()
            if sub:
                pct = sub.percentage
                if pct is not None:
                    percentages.append(pct)
        if not percentages:
            self.average_score = None
            self.status = 'in_progress'
        else:
            self.average_score = round(sum(percentages) / len(percentages), 2)
            if len(percentages) == assignments.count():
                if self.average_score >= settings.PASS_MARK:
                    self.status = 'passed'
                else:
                    self.status = 'failed'
            else:
                self.status = 'in_progress'
        self.save()
        return self.average_score