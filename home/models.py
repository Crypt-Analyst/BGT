from django.core.exceptions import ValidationError
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


class SiteSettings(models.Model):
	site_name = models.CharField(max_length=120, default="Bwire Global Tech")
	tagline = models.CharField(max_length=120, default="The Mind Behind the Machine")
	owner_name = models.CharField(max_length=120, default="Bilford Derick Bwire")
	email = models.EmailField(default="bwireglobaltech917@gmail.com")
	phone = models.CharField(max_length=40, default="0722206805")
	instagram = models.CharField(max_length=120, default="bwireglobaltech")
	tiktok = models.CharField(max_length=120, default="bwireglobaltech")
	whatsapp_number = models.CharField(max_length=20, default="254722206805")
	whatsapp_message = models.CharField(
		max_length=240,
		default="Hi Bwire Global Tech, I'd like to start a project.",
	)
	footer_blurb = models.TextField(
		default="Premium digital systems with a strong visual identity, built for trust, speed, and conversion."
	)
	header_cta_label = models.CharField(max_length=60, default="Start a project")

	def __str__(self) -> str:
		return "Site settings"


class HomeHero(models.Model):
	badge = models.CharField(max_length=120, default="The Mind Behind the Machine")
	title = models.CharField(
		max_length=200,
		default="We build websites first, then AI solutions that support the business.",
	)
	lede = models.TextField(
		default=(
			"Bwire Global Tech focuses on web development, then AI solutions, with added support for dashboards, "
			"cloud setup, and design where needed. The website should reflect real work, not generic filler."
		),
	)
	primary_cta_label = models.CharField(max_length=60, default="Start a project")
	secondary_cta_label = models.CharField(max_length=60, default="See the vision")

	def __str__(self) -> str:
		return "Home hero"


class HomeMetric(models.Model):
	label = models.CharField(max_length=120)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.label


class HomeService(models.Model):
	title = models.CharField(max_length=120)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class HomeCaseStudy(models.Model):
	title = models.CharField(max_length=140)
	body = models.TextField()
	stat_primary = models.CharField(max_length=60, blank=True)
	stat_secondary = models.CharField(max_length=60, blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class MediaAsset(models.Model):
	MEDIA_TYPE_CHOICES = [
		("image", "Image"),
		("video", "Video"),
	]

	media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default="image")
	title = models.CharField(max_length=140, blank=True)
	caption = models.TextField(blank=True)
	image = models.ImageField(upload_to="media/images/", blank=True)
	video = models.FileField(upload_to="media/videos/", blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		abstract = True
		ordering = ["order", "id"]

	def clean(self) -> None:
		if self.media_type == "image" and not self.image:
			raise ValidationError("Image is required when media type is image.")
		if self.media_type == "video" and not self.video:
			raise ValidationError("Video is required when media type is video.")

	def __str__(self) -> str:
		label = self.title or "Media item"
		return f"{label} ({self.media_type})"


class HomeCaseStudyMedia(MediaAsset):
	case_study = models.ForeignKey(
		HomeCaseStudy,
		on_delete=models.CASCADE,
		related_name="media_items",
	)

	def __str__(self) -> str:
		label = self.title or self.case_study.title
		return f"{label} ({self.media_type})"


class HomeTestimonial(models.Model):
	quote = models.TextField()
	author = models.CharField(max_length=120)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.author


class HomeFaq(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.question


class HomeCta(models.Model):
	eyebrow = models.CharField(max_length=120, default="Get started")
	title = models.CharField(max_length=200, default="Send a website brief or an AI idea.")
	body = models.TextField(default="We will turn it into a real project path, not generic filler.")
	button_label = models.CharField(max_length=80, default="Open contact page")

	def __str__(self) -> str:
		return "Home CTA"


class AboutHero(models.Model):
	badge = models.CharField(max_length=120, default="About Bwire Global Tech")
	title = models.CharField(max_length=200)
	lede = models.TextField()

	def __str__(self) -> str:
		return "About hero"


class AboutCard(models.Model):
	SECTION_CHOICES = [
		("mission", "Mission"),
		("vision", "Vision"),
		("what", "What we do"),
		("values", "Why it matters"),
	]
	section = models.CharField(max_length=20, choices=SECTION_CHOICES)
	title = models.CharField(max_length=140)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["section", "order", "id"]

	def __str__(self) -> str:
		return f"{self.section}: {self.title}"


class AboutStep(models.Model):
	title = models.CharField(max_length=140)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class AboutCapability(models.Model):
	label = models.CharField(max_length=80)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.label


class AboutOwner(models.Model):
	name = models.CharField(max_length=120, default="Bilford Derick Bwire")
	role = models.CharField(max_length=120, default="Founder and owner")
	lede = models.TextField()

	def __str__(self) -> str:
		return self.name


class ServicesHero(models.Model):
	badge = models.CharField(max_length=120, default="Services")
	title = models.CharField(max_length=200)
	lede = models.TextField()

	def __str__(self) -> str:
		return "Services hero"


class ServiceItem(models.Model):
	title = models.CharField(max_length=140)
	body = models.TextField()
	bullet_1 = models.CharField(max_length=120, blank=True)
	bullet_2 = models.CharField(max_length=120, blank=True)
	bullet_3 = models.CharField(max_length=120, blank=True)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class DeliverableItem(models.Model):
	title = models.CharField(max_length=140)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class TimelineStep(models.Model):
	step_label = models.CharField(max_length=20, default="01")
	title = models.CharField(max_length=120)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class ServicesFaq(models.Model):
	question = models.CharField(max_length=200)
	answer = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.question


class PricingHero(models.Model):
	badge = models.CharField(max_length=120, default="Pricing")
	title = models.CharField(max_length=200)
	lede = models.TextField()
	ai_note = models.TextField(default="AI solutions: From $700 per project. Custom AI systems are priced by scope.")

	def __str__(self) -> str:
		return "Pricing hero"


class PricingPackage(models.Model):
	name = models.CharField(max_length=120)
	price = models.CharField(max_length=80)
	subtitle = models.CharField(max_length=140, blank=True)
	bullet_1 = models.CharField(max_length=160, blank=True)
	bullet_2 = models.CharField(max_length=160, blank=True)
	bullet_3 = models.CharField(max_length=160, blank=True)
	bullet_4 = models.CharField(max_length=160, blank=True)
	bullet_5 = models.CharField(max_length=160, blank=True)
	bullet_6 = models.CharField(max_length=160, blank=True)
	footer_note = models.CharField(max_length=160, blank=True)
	featured = models.BooleanField(default=False)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.name


class PricingAddon(models.Model):
	name = models.CharField(max_length=120)
	price = models.CharField(max_length=80)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.name


class PricingTerms(models.Model):
	line_one = models.CharField(max_length=200)
	line_two = models.CharField(max_length=200, blank=True)

	def __str__(self) -> str:
		return "Pricing terms"


class PricingCta(models.Model):
	eyebrow = models.CharField(max_length=120, default="Ready to build something powerful?")
	title = models.CharField(max_length=200, default="Start your project or request a quote.")
	primary_label = models.CharField(max_length=80, default="Start Your Project")
	secondary_label = models.CharField(max_length=80, default="Request a Quote")

	def __str__(self) -> str:
		return "Pricing CTA"


class PortfolioHero(models.Model):
	badge = models.CharField(max_length=120, default="Portfolio")
	title = models.CharField(max_length=200)
	lede = models.TextField()

	def __str__(self) -> str:
		return "Portfolio hero"


class PortfolioItem(models.Model):
	label = models.CharField(max_length=120, default="Case study")
	title = models.CharField(max_length=200)
	body = models.TextField()
	bullet_1 = models.CharField(max_length=120, blank=True)
	bullet_2 = models.CharField(max_length=120, blank=True)
	bullet_3 = models.CharField(max_length=120, blank=True)
	featured = models.BooleanField(default=False)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class PortfolioItemMedia(MediaAsset):
	portfolio_item = models.ForeignKey(
		PortfolioItem,
		on_delete=models.CASCADE,
		related_name="media_items",
	)

	def __str__(self) -> str:
		label = self.title or self.portfolio_item.title
		return f"{label} ({self.media_type})"


class PortfolioOutcome(models.Model):
	value = models.CharField(max_length=60)
	label = models.CharField(max_length=120)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.label


class PortfolioDeepDive(models.Model):
	title = models.CharField(max_length=200)
	challenge = models.TextField()
	approach = models.TextField()
	result = models.TextField()

	def __str__(self) -> str:
		return "Portfolio deep dive"


class PortfolioDeepDiveMetric(models.Model):
	value = models.CharField(max_length=60)
	label = models.CharField(max_length=120)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.label


class ContactHero(models.Model):
	badge = models.CharField(max_length=120, default="Start Your Project")
	title = models.CharField(max_length=200)
	lede = models.TextField()
	success_message = models.TextField(
		default="Thanks for reaching out! We have received your project request and will get back to you within 24 hours."
	)

	def __str__(self) -> str:
		return "Contact hero"


class ContactChecklistItem(models.Model):
	label = models.CharField(max_length=160)
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.label


class ContactNextStep(models.Model):
	step_label = models.CharField(max_length=20, default="01")
	title = models.CharField(max_length=120)
	body = models.TextField()
	order = models.PositiveIntegerField(default=0)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return self.title


class TermsPage(models.Model):
	title = models.CharField(max_length=200, default="Terms of Use - Bwire Global Tech (Advanced Version)")
	lede = models.TextField(
		default="These Terms govern your access to and use of our website, services, and digital solutions."
	)
	body = models.TextField()

	def __str__(self) -> str:
		return "Terms page"


class PrivacyPage(models.Model):
	title = models.CharField(max_length=200, default="Privacy Policy - Bwire Global Tech")
	lede = models.TextField(
		default=(
			"This Privacy Policy explains how we collect, use, disclose, and safeguard your information when "
			"you visit our website or use our services."
		)
	)
	body = models.TextField()

	def __str__(self) -> str:
		return "Privacy page"


class GalleryMedia(MediaAsset):
	def __str__(self) -> str:
		label = self.title or "Gallery media"
		return f"{label} ({self.media_type})"
