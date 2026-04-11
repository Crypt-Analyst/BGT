from django.contrib import admin

from .models import (
	AboutCapability,
	AboutCard,
	AboutHero,
	AboutOwner,
	AboutStep,
	ContactChecklistItem,
	ContactHero,
	ContactNextStep,
	DeliverableItem,
	HomeCaseStudy,
	HomeCta,
	HomeFaq,
	HomeHero,
	HomeMetric,
	HomeService,
	HomeTestimonial,
	HomeCaseStudyMedia,
	GalleryMedia,
	PortfolioDeepDive,
	PortfolioDeepDiveMetric,
	PortfolioHero,
	PortfolioItem,
	PortfolioItemMedia,
	PortfolioOutcome,
	PrivacyPage,
	PricingAddon,
	PricingCta,
	PricingHero,
	PricingPackage,
	PricingTerms,
	ProjectRequest,
	ServiceItem,
	ServicesFaq,
	ServicesHero,
	SiteSettings,
	TermsPage,
	TimelineStep,
)


admin.site.site_header = "Bwire Global Tech Admin"
admin.site.site_title = "Bwire Global Tech Admin"
admin.site.index_title = "Project Management"


class HomeCaseStudyMediaInline(admin.TabularInline):
	model = HomeCaseStudyMedia
	extra = 1
	fields = ("media_type", "title", "image", "video", "order")


class PortfolioItemMediaInline(admin.TabularInline):
	model = PortfolioItemMedia
	extra = 1
	fields = ("media_type", "title", "image", "video", "order")


@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
	list_display = ("full_name", "email", "phone", "project_type", "budget_range", "created_at")
	list_filter = ("project_type", "budget_range", "referral_source", "created_at")
	search_fields = ("full_name", "email", "phone", "message")
	ordering = ("-created_at",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
	list_display = ("site_name", "email", "phone")


@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(HomeMetric)
class HomeMetricAdmin(admin.ModelAdmin):
	list_display = ("label", "order")
	ordering = ("order",)


@admin.register(HomeService)
class HomeServiceAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	search_fields = ("title", "body")
	ordering = ("order",)
	fieldsets = (
		(None, {"fields": ("title", "body", "order", "bullet_1", "bullet_2", "bullet_3")}),
	)


@admin.register(HomeCaseStudy)
class HomeCaseStudyAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	ordering = ("order",)
	inlines = (HomeCaseStudyMediaInline,)


@admin.register(HomeTestimonial)
class HomeTestimonialAdmin(admin.ModelAdmin):
	list_display = ("author", "order")
	search_fields = ("author", "testimonial")
	ordering = ("order",)
	fieldsets = (
		(None, {"fields": ("author", "testimonial", "order")}),
	)


@admin.register(HomeFaq)
class HomeFaqAdmin(admin.ModelAdmin):
	list_display = ("question", "order")
	ordering = ("order",)


@admin.register(HomeCta)
class HomeCtaAdmin(admin.ModelAdmin):
	list_display = ("title", "button_label")
	search_fields = ("title", "button_label")
	fieldsets = (
		(None, {"fields": ("title", "button_label", "url")}),
	)


@admin.register(AboutHero)
class AboutHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(AboutCard)
class AboutCardAdmin(admin.ModelAdmin):
	list_display = ("section", "title", "order")
	list_filter = ("section",)
	ordering = ("section", "order")


@admin.register(AboutStep)
class AboutStepAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	ordering = ("order",)


@admin.register(AboutCapability)
class AboutCapabilityAdmin(admin.ModelAdmin):
	list_display = ("label", "order")
	ordering = ("order",)


@admin.register(AboutOwner)
class AboutOwnerAdmin(admin.ModelAdmin):
	list_display = ("name", "role")


@admin.register(ServicesHero)
class ServicesHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	ordering = ("order",)


@admin.register(DeliverableItem)
class DeliverableItemAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	ordering = ("order",)


@admin.register(TimelineStep)
class TimelineStepAdmin(admin.ModelAdmin):
	list_display = ("step_label", "title", "order")
	ordering = ("order",)


@admin.register(ServicesFaq)
class ServicesFaqAdmin(admin.ModelAdmin):
	list_display = ("question", "order")
	ordering = ("order",)


@admin.register(PricingHero)
class PricingHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(PricingPackage)
class PricingPackageAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "featured", "order")
	list_filter = ("featured",)
	search_fields = ("name", "description")
	ordering = ("order",)
	fieldsets = (
		(None, {"fields": ("name", "price", "featured", "order", "description")}),
	)


@admin.register(PricingAddon)
class PricingAddonAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "order")
	ordering = ("order",)


@admin.register(PricingTerms)
class PricingTermsAdmin(admin.ModelAdmin):
	list_display = ("line_one",)


@admin.register(PricingCta)
class PricingCtaAdmin(admin.ModelAdmin):
	list_display = ("title", "primary_label")


@admin.register(PortfolioHero)
class PortfolioHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
	list_display = ("title", "category", "featured", "order")
	list_filter = ("category", "featured")
	search_fields = ("title", "body", "process", "testimonial", "results")
	ordering = ("order",)
	inlines = (PortfolioItemMediaInline,)
	fieldsets = (
		(None, {
			"fields": ("label", "category", "title", "body", "featured", "order")
		}),
		("Bullets", {
			"fields": ("bullet_1", "bullet_2", "bullet_3"),
			"classes": ("collapse",)
		}),
		("Details", {
			"fields": ("process", "testimonial", "results"),
			"classes": ("collapse",)
		}),
	)


@admin.register(PortfolioOutcome)
class PortfolioOutcomeAdmin(admin.ModelAdmin):
	list_display = ("label", "value", "order")
	ordering = ("order",)


@admin.register(PortfolioDeepDive)
class PortfolioDeepDiveAdmin(admin.ModelAdmin):
	list_display = ("title",)


@admin.register(PortfolioDeepDiveMetric)
class PortfolioDeepDiveMetricAdmin(admin.ModelAdmin):
	list_display = ("label", "value", "order")
	ordering = ("order",)


@admin.register(ContactHero)
class ContactHeroAdmin(admin.ModelAdmin):
	list_display = ("badge", "title")


@admin.register(ContactChecklistItem)
class ContactChecklistItemAdmin(admin.ModelAdmin):
	list_display = ("label", "order")
	ordering = ("order",)


@admin.register(ContactNextStep)
class ContactNextStepAdmin(admin.ModelAdmin):
	list_display = ("step_label", "title", "order")
	ordering = ("order",)


@admin.register(TermsPage)
class TermsPageAdmin(admin.ModelAdmin):
	list_display = ("title",)


@admin.register(PrivacyPage)
class PrivacyPageAdmin(admin.ModelAdmin):
	list_display = ("title",)


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
	list_display = ("title", "media_type", "order")
	list_filter = ("media_type",)
	ordering = ("order",)
