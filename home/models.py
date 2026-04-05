from django.db import models


class ProjectRequest(models.Model):
	PROJECT_TYPE_CHOICES = [
		("starter", "Starter Website"),
		("business", "Business Website"),
		("premium", "Premium / E-commerce"),
		("custom", "Custom Tech Solution"),
	]

	BUDGET_CHOICES = [
		("under-30000", "Under Ksh 30,000"),
		("30000-65000", "Ksh 30,000 - 65,000"),
		("65000-120000", "Ksh 65,000 - 120,000"),
		("120000-plus", "Ksh 120,000+"),
		("not-sure", "Not sure yet"),
	]

	REFERRAL_CHOICES = [
		("referral", "Referral"),
		("instagram", "Instagram"),
		("tiktok", "TikTok"),
		("google", "Google"),
		("other", "Other"),
	]

	full_name = models.CharField(max_length=120)
	email = models.EmailField()
	phone = models.CharField(max_length=50)
	project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES)
	message = models.TextField()
	budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
	timeline = models.CharField(max_length=120, blank=True)
	referral_source = models.CharField(max_length=20, choices=REFERRAL_CHOICES, blank=True)
	reference_file = models.FileField(upload_to="project-requests/", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.full_name} - {self.project_type}"
