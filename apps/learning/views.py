from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
import csv
from django.http import HttpResponse

from .models import (
    Cohort, Week, Topic, ReferenceMaterial, Tool, ToolFeature,
    Assignment, RubricCriterion, Submission, Review, ReviewRequest, WeeklyProgress, User
)
from .forms import RegisterForm, SubmissionForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Welcome!')
            return redirect('learning:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name='registration/login.html')(request)


def logout_view(request):
    logout(request)
    return redirect('learning:login')


@login_required
def dashboard(request):
    if not request.user.cohort:
        return render(request, 'learning/dashboard.html', {'no_cohort': True})

    weeks = Week.objects.filter(cohort=request.user.cohort).order_by('number')
    progress = {p.week_id: p for p in WeeklyProgress.objects.filter(learner=request.user)}

    week_rows = []
    next_week_id = None
    for w in weeks:
        unlocked = w.is_unlocked_for(request.user)
        is_next = w.is_next_to_attempt(request.user)
        if is_next and next_week_id is None:
            next_week_id = w.id
        week_rows.append({
            'week': w,
            'unlocked': unlocked,
            'progress': progress.get(w.id),
            'is_next': is_next,
        })

    pending_requests = ReviewRequest.objects.filter(
        reviewer=request.user, status='pending'
    ).count()

    return render(request, 'learning/dashboard.html', {
        'week_rows': week_rows,
        'pass_mark': settings.PASS_MARK,
        'pending_requests': pending_requests,
        'next_week_id': next_week_id,
    })

@login_required
def week_detail(request, week_id):
    week = get_object_or_404(Week, id=week_id, cohort=request.user.cohort)

    if not week.is_unlocked_for(request.user):
        messages.error(
            request,
            f'Week {week.number} is locked. You must pass every previous week first.'
        )
        return redirect('learning:dashboard')

    topics = week.topics.all().prefetch_related('materials')
    tools = week.tools.all().prefetch_related('features')
    assignments = week.assignments.all().prefetch_related('criteria')

    submissions = {s.assignment_id: s for s in Submission.objects.filter(
        learner=request.user, assignment__week=week
    )}

    return render(request, 'learning/week_detail.html', {
        'week': week,
        'topics': topics,
        'tools': tools,
        'assignments': assignments,
        'submissions': submissions,
    })

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, week__cohort=request.user.cohort)
    if not topic.week.is_unlocked_for(request.user):
        messages.error(request, 'This week is locked.')
        return redirect('learning:dashboard')
    materials = topic.materials.all()
    return render(request, 'learning/topic_detail.html', {'topic': topic, 'materials': materials})


@login_required
def tool_detail(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id, week__cohort=request.user.cohort)
    if not tool.week.is_unlocked_for(request.user):
        messages.error(request, 'This week is locked.')
        return redirect('learning:dashboard')
    features = tool.features.all()
    assignments = tool.assignments.all()
    submissions = {s.assignment_id: s for s in Submission.objects.filter(
        learner=request.user, assignment__tool=tool
    )}
    return render(request, 'learning/tool_detail.html', {
        'tool': tool,
        'features': features,
        'assignments': assignments,
        'submissions': submissions,
    })


@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, week__cohort=request.user.cohort)
    week = assignment.week
    if not week.is_unlocked_for(request.user):
        messages.error(request, 'This week is locked.')
        return redirect('learning:dashboard')

    submission = Submission.objects.filter(assignment=assignment, learner=request.user).first()

    review_request = None
    if submission:
        review_request = submission.review_requests.first()

    # Whether the user arrived here from the "Reviews I've Given" page.
    # In that case, we don't let them attempt or edit this assignment from this angle.
    from_review = request.GET.get('from') == 'review'

    return render(request, 'learning/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
        'review_request': review_request,
        'from_review': from_review,
    })

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, week__cohort=request.user.cohort)
    if not assignment.week.is_unlocked_for(request.user):
        messages.error(request, 'This week is locked.')
        return redirect('learning:dashboard')

    existing = Submission.objects.filter(assignment=assignment, learner=request.user).first()

    # Fetch eligible reviewers: other learners in the same cohort
    eligible_reviewers = User.objects.filter(
        cohort=request.user.cohort, role='learner'
    ).exclude(id=request.user.id)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=existing)
        reviewer_id = request.POST.get('reviewer')
        if form.is_valid():
            if not reviewer_id:
                messages.error(request, 'Please choose a reviewer.')
            else:
                reviewer = get_object_or_404(
                    User, id=reviewer_id, cohort=request.user.cohort
                )
                sub = form.save(commit=False)
                sub.assignment = assignment
                sub.learner = request.user
                sub.reviewer = reviewer
                sub.status = 'pending'
                sub.save()

                # Handle the review request: create or update
                existing_request = ReviewRequest.objects.filter(submission=sub).first()
                if existing_request:
                    existing_request.reviewer = reviewer
                    existing_request.status = 'pending'
                    existing_request.responded_at = None
                    existing_request.save()
                else:
                    ReviewRequest.objects.create(
                        submission=sub, requester=request.user, reviewer=reviewer
                    )

                _recompute_weekly_progress(request.user, assignment.week)
                messages.success(request, f'Submission saved. {reviewer.get_full_name() or reviewer.username} will be asked to review it.')
                return redirect('learning:assignment_detail', assignment_id=assignment.id)
    else:
        form = SubmissionForm(instance=existing)

    return render(request, 'learning/submit_assignment.html', {
        'assignment': assignment,
        'form': form,
        'existing': existing,
        'eligible_reviewers': eligible_reviewers,
        'existing_reviewer_id': existing.reviewer_id if existing else None,
    })


@login_required
def delete_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, learner=request.user)
    if submission.reviews.filter(is_valid=True).exists():
        messages.error(request, 'Cannot delete a submission that has been reviewed.')
        return redirect('learning:assignment_detail', assignment_id=submission.assignment.id)
    if request.method == 'POST':
        week = submission.assignment.week
        ReviewRequest.objects.filter(submission=submission).delete()
        submission.delete()
        _recompute_weekly_progress(request.user, week)
        messages.success(request, 'Submission deleted.')
        return redirect('learning:week_detail', week_id=week.id)
    return render(request, 'learning/delete_submission.html', {'submission': submission})


# ---------------------------------------------------------------
# INBOX: requests received (accept / reject)
# ---------------------------------------------------------------

@login_required
def review_inbox(request):
    """Where a learner sees requests sent to them and can accept/reject."""
    pending = ReviewRequest.objects.filter(
        reviewer=request.user, status='pending'
    ).select_related('submission__assignment', 'requester')
    accepted = ReviewRequest.objects.filter(
        reviewer=request.user, status='accepted'
    ).select_related('submission__assignment', 'requester')
    completed = ReviewRequest.objects.filter(
        reviewer=request.user, status='completed'
    ).select_related('submission__assignment', 'requester')[:10]

    return render(request, 'learning/review_inbox.html', {
        'pending': pending,
        'accepted': accepted,
        'completed': completed,
    })


@login_required
def accept_review_request(request, request_id):
    rr = get_object_or_404(ReviewRequest, id=request_id, reviewer=request.user)
    if rr.status != 'pending':
        messages.info(request, 'This request has already been handled.')
        return redirect('learning:review_inbox')
    if request.method == 'POST':
        rr.status = 'accepted'
        rr.responded_at = timezone.now()
        rr.save()
        messages.success(request, 'Request accepted. You can now review this submission.')
        return redirect('learning:review_submission', submission_id=rr.submission.id)
    return render(request, 'learning/accept_request.html', {'rr': rr})


@login_required
def reject_review_request(request, request_id):
    rr = get_object_or_404(ReviewRequest, id=request_id, reviewer=request.user)
    if rr.status != 'pending':
        messages.info(request, 'This request has already been handled.')
        return redirect('learning:review_inbox')
    if request.method == 'POST':
        rr.status = 'rejected'
        rr.responded_at = timezone.now()
        rr.save()
        messages.info(request, 'Request rejected. The requester will need to pick a new reviewer.')
        return redirect('learning:review_inbox')
    return render(request, 'learning/reject_request.html', {'rr': rr})


# ---------------------------------------------------------------
# REVIEW
# ---------------------------------------------------------------

@login_required
def review_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)

    # Only the assigned reviewer can review, and only if accepted
    if submission.reviewer_id != request.user.id:
        messages.error(request, 'You are not the assigned reviewer for this submission.')
        return redirect('learning:review_inbox')

    rr = submission.review_requests.first()
    if not rr or rr.status not in ('accepted', 'completed'):
        messages.error(request, 'You must accept the review request before reviewing.')
        return redirect('learning:review_inbox')

    criteria = submission.assignment.criteria.all()
    existing_review = Review.objects.filter(submission=submission, reviewer=request.user).first()

    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        criterion_scores = {}
        for c in criteria:
            raw = request.POST.get(f'criterion_{c.id}')
            if raw is not None:
                try:
                    val = float(raw)
                    val = max(0, min(val, c.max_score))
                    criterion_scores[str(c.id)] = val
                except (ValueError, TypeError):
                    criterion_scores[str(c.id)] = 0

        if len(comment) < settings.MIN_REVIEW_COMMENT_LENGTH:
            messages.error(request, f'Your comment must be at least {settings.MIN_REVIEW_COMMENT_LENGTH} characters.')
        else:
            review, _ = Review.objects.update_or_create(
                submission=submission,
                reviewer=request.user,
                defaults={'comment': comment, 'criterion_scores': criterion_scores}
            )
            review.save()
            submission.status = 'reviewed'
            submission.save()
            rr.status = 'completed'
            rr.save()
            _recompute_weekly_progress(submission.learner, submission.assignment.week)
            messages.success(request, 'Review submitted. Thank you!')
            return redirect('learning:review_inbox')

    return render(request, 'learning/review_submission.html', {
        'submission': submission,
        'criteria': criteria,
        'existing_review': existing_review,
    })


# ---------------------------------------------------------------
# OUTGOING: what I sent to others
# ---------------------------------------------------------------

@login_required
def my_requests(request):
    """Requests the current user has sent."""
    sent = ReviewRequest.objects.filter(requester=request.user).select_related(
        'submission__assignment', 'reviewer'
    )
    return render(request, 'learning/my_requests.html', {'sent': sent})


# ---------------------------------------------------------------
# Transcript, Profile
# ---------------------------------------------------------------
@login_required
def transcript(request):
    """Full transcript with per-week breakdown, overall summary, and CSV download."""
    if not request.user.cohort:
        return render(request, 'learning/transcript.html', {'no_cohort': True})

    weeks = Week.objects.filter(cohort=request.user.cohort).order_by('number')

    def letter_of(score):
        if score is None:
            return '—'
        if score >= 75:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 50:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'E'

    rows = []
    all_scores = []
    total_assignments = 0
    graded_assignments = 0
    passed_weeks = 0
    failed_weeks = 0

    for w in weeks:
        progress = WeeklyProgress.objects.filter(learner=request.user, week=w).first()
        assignment_rows = []
        for a in w.assignments.all():
            sub = Submission.objects.filter(assignment=a, learner=request.user).first()
            score = sub.percentage if sub else None
            if sub:
                total_assignments += 1
                if score is not None:
                    graded_assignments += 1
                    all_scores.append(score)
            assignment_rows.append({
                'assignment': a,
                'submission': sub,
                'score': score,
            })
        if progress:
            if progress.status == 'passed':
                passed_weeks += 1
            elif progress.status == 'failed':
                failed_weeks += 1
        rows.append({
            'week': w,
            'progress': progress,
            'assignments': assignment_rows,
        })

    overall_average = round(sum(all_scores) / len(all_scores), 2) if all_scores else 0

    summary = {
        'overall_average': overall_average,
        'overall_letter': letter_of(overall_average) if all_scores else '—',
        'total_weeks': weeks.count(),
        'passed_weeks': passed_weeks,
        'failed_weeks': failed_weeks,
        'total_assignments': total_assignments,
        'graded_assignments': graded_assignments,
    }

    # CSV download
    if 'download' in request.GET:
        response = HttpResponse(content_type='text/csv')
        filename = f'transcript_{request.user.username}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Student', request.user.get_full_name() or request.user.username])
        writer.writerow(['Cohort', request.user.cohort.name])
        writer.writerow(['Overall Average', f'{overall_average}%'])
        writer.writerow(['Overall Grade', summary['overall_letter']])
        writer.writerow(['Weeks Passed', f'{passed_weeks}/{weeks.count()}'])
        writer.writerow([])
        writer.writerow([
            'Week #', 'Week Title', 'Assignment', 'Submitted', 'Reviewer',
            'Score %', 'Grade', 'Feedback', 'Week Average', 'Week Status'
        ])
        for row in rows:
            w = row['week']
            progress = row['progress']
            if progress and progress.average_score is not None:
                avg_cell = f'{progress.average_score:.1f}'
                status_cell = progress.status
            else:
                avg_cell = ''
                status_cell = 'not_started'
            for ar in row['assignments']:
                sub = ar['submission']
                score = ar['score']
                letter = letter_of(score) if score is not None else ''
                score_cell = f'{score:.1f}' if score is not None else ''
                writer.writerow([
                    w.number,
                    w.title,
                    ar['assignment'].title,
                    sub.submitted_at.date() if sub else '',
                    (sub.reviewer.get_full_name() or sub.reviewer.username) if sub and sub.reviewer else '',
                    score_cell,
                    letter,
                    sub.review.comment if sub and sub.review else '',
                    avg_cell,
                    status_cell,
                ])
        return response

    return render(request, 'learning/transcript.html', {
        'rows': rows,
        'summary': summary,
        'pass_mark': settings.PASS_MARK,
    })


@login_required
def reviews_given(request):
    """All reviews this learner has given to others, with the work they saw and their score."""
    reviews = Review.objects.filter(reviewer=request.user).select_related(
        'submission__assignment__week', 'submission__learner'
    ).order_by('-reviewed_at')

    return render(request, 'learning/reviews_given.html', {'reviews': reviews})

@login_required
def profile(request):
    return render(request, 'learning/profile.html', {'user': request.user})


# ---------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------

def _recompute_weekly_progress(learner, week):
    progress, _ = WeeklyProgress.objects.get_or_create(learner=learner, week=week)
    progress.compute()