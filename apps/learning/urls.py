from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------- Password reset ----------
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/password-reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/password-reset/complete/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),

    # ---------- Learning content ----------
    path('week/<int:week_id>/', views.week_detail, name='week_detail'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('tool/<int:tool_id>/', views.tool_detail, name='tool_detail'),

    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submission/<int:submission_id>/delete/', views.delete_submission, name='delete_submission'),

    path('requests/inbox/', views.review_inbox, name='review_inbox'),
    path('requests/sent/', views.my_requests, name='my_requests'),
    path('requests/<int:request_id>/accept/', views.accept_review_request, name='accept_request'),
    path('requests/<int:request_id>/reject/', views.reject_review_request, name='reject_request'),

    path('review/<int:submission_id>/', views.review_submission, name='review_submission'),

    path('transcript/', views.transcript, name='transcript'),
    path('reviews-given/', views.reviews_given, name='reviews_given'),

    path('profile/', views.profile, name='profile'),
]