from django.contrib import admin

from .models import ProjectRequest


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
	list_display = ("full_name", "email", "phone", "project_type", "budget_range", "created_at")
	list_filter = ("project_type", "budget_range", "referral_source", "created_at")
	search_fields = ("full_name", "email", "phone", "message")
	ordering = ("-created_at",)
