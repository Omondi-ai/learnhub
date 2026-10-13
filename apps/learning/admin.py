from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Cohort, Week, Topic, ReferenceMaterial, Tool, ToolFeature,
    Assignment, RubricCriterion, PeerPairing, Submission, Review,
    ReviewRequest, WeeklyProgress
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'cohort')
    list_filter = ('role', 'cohort')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Platform', {'fields': ('role', 'cohort')}),
    )


admin.site.register(Cohort)
admin.site.register(Week)
admin.site.register(Topic)
admin.site.register(ReferenceMaterial)
admin.site.register(Tool)
admin.site.register(ToolFeature)


class RubricCriterionInline(admin.TabularInline):
    model = RubricCriterion
    extra = 1


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'week', 'tool', 'submission_type', 'is_open_ended')
    list_filter = ('week', 'submission_type')
    inlines = [RubricCriterionInline]


@admin.register(PeerPairing)
class PeerPairingAdmin(admin.ModelAdmin):
    list_display = ('week', 'learner_a', 'learner_b', 'created_at')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('learner', 'assignment', 'reviewer', 'status', 'submitted_at')
    list_filter = ('status', 'assignment__week')
    search_fields = ('learner__username', 'assignment__title')


@admin.register(ReviewRequest)
class ReviewRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'reviewer', 'submission', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('requester__username', 'reviewer__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('submission', 'reviewer', 'total_score', 'is_valid', 'reviewed_at')
    list_filter = ('is_valid',)


@admin.register(WeeklyProgress)
class WeeklyProgressAdmin(admin.ModelAdmin):
    list_display = ('learner', 'week', 'average_score', 'status', 'computed_at')
    list_filter = ('status', 'week')