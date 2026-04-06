from django.core.management.base import BaseCommand

from home.models import (
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
    PortfolioDeepDive,
    PortfolioDeepDiveMetric,
    PortfolioHero,
    PortfolioItem,
    PortfolioOutcome,
    PrivacyPage,
    PricingAddon,
    PricingCta,
    PricingHero,
    PricingPackage,
    PricingTerms,
    ServiceItem,
    ServicesFaq,
    ServicesHero,
    SiteSettings,
    TermsPage,
    TimelineStep,
)


class Command(BaseCommand):
    help = "Seed CMS content with the current site defaults."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Bwire Global Tech",
                "tagline": "The Mind Behind the Machine",
                "owner_name": "Bilford Derick Bwire",
                "email": "bwireglobaltech917@gmail.com",
                "phone": "0722206805",
                "instagram": "bwireglobaltech",
                "tiktok": "bwireglobaltech",
                "whatsapp_number": "254722206805",
                "whatsapp_message": "Hi Bwire Global Tech, I'd like to start a project.",
                "footer_blurb": (
                    "Premium digital systems with a strong visual identity, built for trust, speed, and conversion."
                ),
                "header_cta_label": "Start a project",
            },
        )

        HomeHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "The Mind Behind the Machine",
                "title": "We build websites first, then AI solutions that support the business.",
                "lede": (
                    "Bwire Global Tech focuses on web development, then AI solutions, with added support for "
                    "dashboards, cloud setup, and design where needed. The website should reflect real work, "
                    "not generic filler."
                ),
                "primary_cta_label": "Start a project",
                "secondary_cta_label": "See the vision",
            },
        )

        if not HomeMetric.objects.exists():
            HomeMetric.objects.bulk_create(
                [
                    HomeMetric(label="Web development", order=1),
                    HomeMetric(label="AI solutions", order=2),
                    HomeMetric(label="Dashboards and support", order=3),
                ]
            )

        if not HomeService.objects.exists():
            HomeService.objects.bulk_create(
                [
                    HomeService(
                        title="Web development",
                        body=(
                            "Company websites, landing pages, portals, and dashboards built with Django, HTML, CSS, "
                            "and JavaScript."
                        ),
                        order=1,
                    ),
                    HomeService(
                        title="AI solutions",
                        body=(
                            "Practical AI tools, assistants, and BwiResQ-style ideas that help businesses work faster "
                            "and smarter."
                        ),
                        order=2,
                    ),
                    HomeService(
                        title="Support services",
                        body=(
                            "Cloud setup, dashboards, maintenance, and design support that keep the website useful "
                            "after launch."
                        ),
                        order=3,
                    ),
                ]
            )

        if not HomeCaseStudy.objects.exists():
            HomeCaseStudy.objects.bulk_create(
                [
                    HomeCaseStudy(
                        title="Corporate rebrand site",
                        body="Rebuilt structure, sharpened messaging, and delivered a conversion-first layout.",
                        stat_primary="+42% engagement",
                        stat_secondary="+31% inquiries",
                        order=1,
                    ),
                    HomeCaseStudy(
                        title="AI services launch",
                        body="Focused offer, clear CTA, and a fast landing experience for lead capture.",
                        stat_primary="2.1s load time",
                        stat_secondary="3x CTA taps",
                        order=2,
                    ),
                    HomeCaseStudy(
                        title="Business systems hub",
                        body="Unified services, support, and product pages into a clean navigation system.",
                        stat_primary="12 new pages",
                        stat_secondary="100% brand consistency",
                        order=3,
                    ),
                ]
            )

        if not HomeTestimonial.objects.exists():
            HomeTestimonial.objects.bulk_create(
                [
                    HomeTestimonial(
                        quote="The site feels premium and converts better. The web-first strategy delivered instantly.",
                        author="CEO, Fintech Studio",
                        order=1,
                    ),
                    HomeTestimonial(
                        quote="Fast delivery, sharp visuals, and a clear roadmap for AI enhancements.",
                        author="Product Lead, Health Startup",
                        order=2,
                    ),
                    HomeTestimonial(
                        quote="Their structure and copy made our offer easy to understand in seconds.",
                        author="Founder, Consulting Firm",
                        order=3,
                    ),
                ]
            )

        if not HomeFaq.objects.exists():
            HomeFaq.objects.bulk_create(
                [
                    HomeFaq(
                        question="Do you build websites only, or apps too?",
                        answer=(
                            "We build more than just websites. At Bwire Global Tech, we develop:\n"
                            "Professional websites\n"
                            "Web applications & custom systems\n"
                            "AI-powered solutions\n"
                            "Data-driven platforms\n\n"
                            "Whether it is a simple site or a complex system, we tailor everything to your needs."
                        ),
                        order=1,
                    ),
                    HomeFaq(
                        question="When does AI work start?",
                        answer=(
                            "AI projects begin after a clear understanding of your requirements.\n\n"
                            "First, we review your idea and data\n"
                            "Then define the scope and solution\n"
                            "Development starts immediately after agreement and initial payment\n\n"
                            "Every AI project is customized to solve a specific problem, so planning is key."
                        ),
                        order=2,
                    ),
                    HomeFaq(
                        question="How fast can you deliver?",
                        answer=(
                            "Delivery depends on the package and project complexity:\n\n"
                            "Starter websites: 5-7 days\n"
                            "Business websites: 10-14 days\n"
                            "Premium / E-commerce: 2-4 weeks\n\n"
                            "For urgent projects, faster delivery may be arranged upon request."
                        ),
                        order=3,
                    ),
                ]
            )

        HomeCta.objects.get_or_create(
            pk=1,
            defaults={
                "eyebrow": "Get started",
                "title": "Send a website brief or an AI idea.",
                "body": "We will turn it into a real project path, not generic filler.",
                "button_label": "Open contact page",
            },
        )

        AboutHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "About Bwire Global Tech",
                "title": "Innovative digital solutions that empower modern businesses.",
                "lede": (
                    "At Bwire Global Tech, we are passionate about building digital solutions that help businesses "
                    "grow, scale, and succeed in a fast-changing technological world."
                ),
            },
        )

        if not AboutCard.objects.exists():
            AboutCard.objects.bulk_create(
                [
                    AboutCard(
                        section="mission",
                        title="Deliver smart, reliable, and impactful technology that solves real problems.",
                        body="We design technology that creates opportunity and turns vision into results.",
                        order=1,
                    ),
                    AboutCard(
                        section="vision",
                        title="Help businesses grow, scale, and lead with technology that performs.",
                        body=(
                            "From small startups to growing enterprises, we build solutions that drive measurable "
                            "impact."
                        ),
                        order=2,
                    ),
                    AboutCard(
                        section="what",
                        title="Web development",
                        body="Modern websites and platforms built to convert, scale, and perform.",
                        order=1,
                    ),
                    AboutCard(
                        section="what",
                        title="Artificial intelligence",
                        body="AI automation and assistants designed to deliver real business value.",
                        order=2,
                    ),
                    AboutCard(
                        section="what",
                        title="Data science",
                        body="Insights and analytics that turn data into confident decisions.",
                        order=3,
                    ),
                    AboutCard(
                        section="what",
                        title="Cybersecurity",
                        body="Security-first protection for digital systems and operations.",
                        order=4,
                    ),
                    AboutCard(
                        section="what",
                        title="Cloud and delivery",
                        body="Reliable deployments and infrastructure that keep systems fast and stable.",
                        order=5,
                    ),
                    AboutCard(
                        section="what",
                        title="Design and UX",
                        body="Clean, user-friendly experiences built to match brand identity.",
                        order=6,
                    ),
                    AboutCard(
                        section="values",
                        title="Problem solving",
                        body="We focus on real challenges that need smart, practical solutions.",
                        order=1,
                    ),
                    AboutCard(
                        section="values",
                        title="Opportunities",
                        body="Every build is designed to unlock growth and new possibilities.",
                        order=2,
                    ),
                    AboutCard(
                        section="values",
                        title="Impact",
                        body="We turn ideas into digital experiences that make a lasting difference.",
                        order=3,
                    ),
                ]
            )

        if not AboutStep.objects.exists():
            AboutStep.objects.bulk_create(
                [
                    AboutStep(
                        title="Understand the vision",
                        body="We learn your goals, challenges, and the impact you want to make.",
                        order=1,
                    ),
                    AboutStep(
                        title="Design with purpose",
                        body="Every screen and workflow is crafted to solve the right problem.",
                        order=2,
                    ),
                    AboutStep(
                        title="Build with precision",
                        body="Clean builds, strong performance, and scalable systems that last.",
                        order=3,
                    ),
                    AboutStep(
                        title="Deliver with excellence",
                        body="We deliver with care, clarity, and long-term support.",
                        order=4,
                    ),
                ]
            )

        if not AboutCapability.objects.exists():
            AboutCapability.objects.bulk_create(
                [
                    AboutCapability(label="Web development", order=1),
                    AboutCapability(label="Artificial intelligence", order=2),
                    AboutCapability(label="Data science", order=3),
                    AboutCapability(label="Cybersecurity", order=4),
                    AboutCapability(label="UI strategy", order=5),
                    AboutCapability(label="Cloud delivery", order=6),
                    AboutCapability(label="Automation", order=7),
                    AboutCapability(label="Maintenance", order=8),
                ]
            )

        AboutOwner.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Bilford Derick Bwire",
                "role": "Founder and owner",
                "lede": (
                    "Founder and owner of Bwire Global Tech, guiding the brand across web development, AI, and "
                    "modern digital systems."
                ),
            },
        )

        ServicesHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "Services",
                "title": "Web development is the main service. AI is the second focus.",
                "lede": (
                    "Bwire Global Tech mainly builds websites and web apps, then adds AI solutions or support work "
                    "when needed."
                ),
            },
        )

        if not ServiceItem.objects.exists():
            ServiceItem.objects.bulk_create(
                [
                    ServiceItem(
                        title="Software development",
                        body=(
                            "Fast, responsive websites and web apps built to support visibility, leads, and operations."
                        ),
                        bullet_1="Landing pages",
                        bullet_2="Business portals",
                        bullet_3="Internal tools",
                        order=1,
                    ),
                    ServiceItem(
                        title="AI solutions",
                        body=(
                            "AI ideas, assistants, dashboards, and data workflows that help businesses work faster "
                            "and smarter."
                        ),
                        bullet_1="Predictive models",
                        bullet_2="BwiResQ AI ideas",
                        bullet_3="Smart analytics",
                        order=2,
                    ),
                    ServiceItem(
                        title="Support services",
                        body=(
                            "Cloud setup, security reviews, maintenance, and design support for live websites and "
                            "systems."
                        ),
                        bullet_1="Cloud setup",
                        bullet_2="Security checks",
                        bullet_3="Maintenance plans",
                        order=3,
                    ),
                    ServiceItem(
                        title="Design and dashboards",
                        body=(
                            "Visual identity, UI polish, and reporting dashboards that support the web product and the "
                            "brand."
                        ),
                        bullet_1="Graphic design",
                        bullet_2="Dashboards",
                        bullet_3="UI support",
                        order=4,
                    ),
                ]
            )

        if not DeliverableItem.objects.exists():
            DeliverableItem.objects.bulk_create(
                [
                    DeliverableItem(
                        title="Production-ready site",
                        body="Responsive layout, clear navigation, and a conversion-first structure.",
                        order=1,
                    ),
                    DeliverableItem(
                        title="Performance baseline",
                        body="Optimized load speed, asset compression, and SEO-ready metadata.",
                        order=2,
                    ),
                    DeliverableItem(
                        title="Growth roadmap",
                        body="AI or dashboard enhancements planned after the site proves itself.",
                        order=3,
                    ),
                ]
            )

        if not TimelineStep.objects.exists():
            TimelineStep.objects.bulk_create(
                [
                    TimelineStep(
                        step_label="01",
                        title="Discover",
                        body="Gather the website goals, page structure, and any AI features needed.",
                        order=1,
                    ),
                    TimelineStep(
                        step_label="02",
                        title="Design",
                        body=(
                            "Build pages and components with a strong mobile-friendly layout and clear conversion "
                            "path."
                        ),
                        order=2,
                    ),
                    TimelineStep(
                        step_label="03",
                        title="Launch",
                        body="Deploy the site and then refine content, performance, and the contact flow.",
                        order=3,
                    ),
                ]
            )

        if not ServicesFaq.objects.exists():
            ServicesFaq.objects.bulk_create(
                [
                    ServicesFaq(
                        question="Do you offer maintenance?",
                        answer="Yes. We provide post-launch support, updates, and security check-ins.",
                        order=1,
                    ),
                    ServicesFaq(
                        question="Can you redesign an existing site?",
                        answer="Yes. We can refresh messaging, structure, and UI while keeping your content.",
                        order=2,
                    ),
                    ServicesFaq(
                        question="What do you need to start?",
                        answer="Business goals, examples you admire, and any launch deadlines.",
                        order=3,
                    ),
                ]
            )

        PricingHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "Pricing",
                "title": "Build smarter. Launch faster.",
                "lede": (
                    "Choose a package designed to move your business forward. From simple websites to powerful "
                    "digital systems, we have you covered."
                ),
                "ai_note": "AI solutions: From $700 per project. Custom AI systems are priced by scope.",
            },
        )

        if not PricingPackage.objects.exists():
            PricingPackage.objects.bulk_create(
                [
                    PricingPackage(
                        name="Starter",
                        price="Ksh 30,000",
                        subtitle="Perfect for getting online quickly",
                        bullet_1="Clean 3-5 page website",
                        bullet_2="Fully responsive (mobile and desktop)",
                        bullet_3="Contact and WhatsApp integration",
                        bullet_4="Basic SEO setup",
                        bullet_5="Fast delivery: 5-7 days",
                        footer_note="Ideal for startups and small businesses.",
                        featured=False,
                        order=1,
                    ),
                    PricingPackage(
                        name="Business",
                        price="Ksh 65,000",
                        subtitle="Built to grow your brand and attract clients",
                        bullet_1="6-10 professional pages",
                        bullet_2="CMS (manage your content easily)",
                        bullet_3="Blog and SEO optimization",
                        bullet_4="Google Analytics integration",
                        bullet_5="Domain and hosting setup",
                        bullet_6="Delivery: 10-14 days",
                        footer_note="Best for businesses ready to scale.",
                        featured=True,
                        order=2,
                    ),
                    PricingPackage(
                        name="Premium",
                        price="Ksh 120,000",
                        subtitle="Powerful, scalable, and revenue-focused",
                        bullet_1="Unlimited pages",
                        bullet_2="Full e-commerce system",
                        bullet_3="M-Pesa and card payments",
                        bullet_4="Custom features and design",
                        bullet_5="Advanced SEO",
                        bullet_6="Admin dashboard",
                        footer_note="For serious brands and online stores.",
                        featured=False,
                        order=3,
                    ),
                ]
            )

        if not PricingAddon.objects.exists():
            PricingAddon.objects.bulk_create(
                [
                    PricingAddon(name="Domain", price="Ksh 1,500 - 3,000 / year", order=1),
                    PricingAddon(name="Hosting", price="Ksh 5,000 - 10,000 / year", order=2),
                    PricingAddon(name="Maintenance", price="Ksh 3,000 - 5,000 / month", order=3),
                    PricingAddon(name="SEO", price="Ksh 10,000 - 20,000", order=4),
                    PricingAddon(name="Extra pages", price="Ksh 1,500 / page", order=5),
                ]
            )

        PricingTerms.objects.get_or_create(
            pk=1,
            defaults={
                "line_one": "50% deposit required to start. Remaining balance after completion.",
                "line_two": "Pricing may vary based on requirements.",
            },
        )

        PricingCta.objects.get_or_create(
            pk=1,
            defaults={
                "eyebrow": "Ready to build something powerful?",
                "title": "Start your project or request a quote.",
                "primary_label": "Start Your Project",
                "secondary_label": "Request a Quote",
            },
        )

        PortfolioHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "Portfolio",
                "title": "Sample outcomes for a premium tech brand.",
                "lede": (
                    "These project cards show the kind of story the site should tell: clear problem, strong visual "
                    "identity, measurable result."
                ),
            },
        )

        if not PortfolioItem.objects.exists():
            PortfolioItem.objects.bulk_create(
                [
                    PortfolioItem(
                        label="Case study 01",
                        title="Corporate rebrand website",
                        body=(
                            "Translated a technical company identity into a premium web presence with stronger "
                            "structure and better conversion flow."
                        ),
                        bullet_1="Brand refresh",
                        bullet_2="Responsive layout",
                        bullet_3="Lead generation",
                        featured=True,
                        order=1,
                    ),
                    PortfolioItem(
                        label="Case study 02",
                        title="AI services landing page",
                        body=(
                            "A focused page that explained the offer quickly, used strong typography, and directed "
                            "users to book a discovery call."
                        ),
                        bullet_1="Clear offer",
                        bullet_2="Fast loading",
                        bullet_3="CTA focused",
                        featured=False,
                        order=2,
                    ),
                    PortfolioItem(
                        label="Case study 03",
                        title="Business systems hub",
                        body=(
                            "A page hierarchy that organized services, support, and product information into easy-to-"
                            "scan sections."
                        ),
                        bullet_1="Information design",
                        bullet_2="Navigation clarity",
                        bullet_3="Scalable sections",
                        featured=False,
                        order=3,
                    ),
                ]
            )

        if not PortfolioOutcome.objects.exists():
            PortfolioOutcome.objects.bulk_create(
                [
                    PortfolioOutcome(value="+42%", label="Longer engagement", order=1),
                    PortfolioOutcome(value="+31%", label="More inquiries", order=2),
                    PortfolioOutcome(value="100%", label="Brand consistency", order=3),
                ]
            )

        PortfolioDeepDive.objects.get_or_create(
            pk=1,
            defaults={
                "title": "Corporate rebrand website",
                "challenge": "an outdated site that failed to communicate trust and capability.",
                "approach": "rebuilt the story, tightened the CTA, and introduced a consistent visual system.",
                "result": "a cleaner experience with stronger engagement and higher inquiry rate.",
            },
        )

        if not PortfolioDeepDiveMetric.objects.exists():
            PortfolioDeepDiveMetric.objects.bulk_create(
                [
                    PortfolioDeepDiveMetric(value="+42%", label="Engagement", order=1),
                    PortfolioDeepDiveMetric(value="+31%", label="Inquiries", order=2),
                    PortfolioDeepDiveMetric(value="2.1s", label="Load time", order=3),
                ]
            )

        ContactHero.objects.get_or_create(
            pk=1,
            defaults={
                "badge": "Start Your Project",
                "title": "Let's build something amazing together.",
                "lede": (
                    "At Bwire Global Tech, we turn your ideas into powerful digital solutions. Whether you need a "
                    "professional website, an e-commerce store, or a custom tech solution, we are here to make it "
                    "happen. Fill out the form below and let's get your project started."
                ),
                "success_message": (
                    "Thanks for reaching out! We have received your project request and will get back to you within "
                    "24 hours."
                ),
            },
        )

        if not ContactChecklistItem.objects.exists():
            ContactChecklistItem.objects.bulk_create(
                [
                    ContactChecklistItem(label="Your business name", order=1),
                    ContactChecklistItem(label="Website goals", order=2),
                    ContactChecklistItem(label="AI feature idea if needed", order=3),
                    ContactChecklistItem(label="Budget range (optional)", order=4),
                    ContactChecklistItem(label="Deadline or launch date", order=5),
                ]
            )

        if not ContactNextStep.objects.exists():
            ContactNextStep.objects.bulk_create(
                [
                    ContactNextStep(
                        step_label="01",
                        title="Review",
                        body="We read your brief and map the right web-first direction.",
                        order=1,
                    ),
                    ContactNextStep(
                        step_label="02",
                        title="Call",
                        body="We schedule a short call to confirm scope and timeline.",
                        order=2,
                    ),
                    ContactNextStep(
                        step_label="03",
                        title="Proposal",
                        body="You receive a clear proposal with deliverables and next steps.",
                        order=3,
                    ),
                ]
            )

        terms_defaults = {
            "title": "Terms of Use - Bwire Global Tech (Advanced Version)",
            "lede": "These Terms govern your access to and use of our website, services, and digital solutions.",
            "body": (
                    "<h2>1. Introduction</h2>"
                    "<p>Welcome to Bwire Global Tech. These Terms of Use (\"Terms\") govern your access to and use "
                    "of our website, services, and digital solutions. By accessing or using our website, you agree "
                    "to be legally bound by these Terms. If you do not agree, you must not use our services.</p>"
                    "<h2>2. Definitions</h2>"
                    "<ul>"
                    "<li>\"Company\" refers to Bwire Global Tech</li>"
                    "<li>\"Client\" / \"User\" refers to any individual or entity using our services</li>"
                    "<li>\"Services\" include web development, AI solutions, data science, cybersecurity, and digital systems</li>"
                    "<li>\"Website\" refers to all pages under our domain</li>"
                    "</ul>"
                    "<h2>3. Eligibility</h2>"
                    "<p>You must be at least 18 years old or have legal authority to enter into agreements to use our services.</p>"
                    "<h2>4. Scope of Services</h2>"
                    "<p>Bwire Global Tech provides digital services including but not limited to:</p>"
                    "<ul>"
                    "<li>Website design and development</li>"
                    "<li>AI and data-driven systems</li>"
                    "<li>Cloud and web solutions</li>"
                    "<li>Cybersecurity services</li>"
                    "</ul>"
                    "<p>All services are delivered based on agreed project specifications.</p>"
                    "<h2>5. User Responsibilities</h2>"
                    "<p>You agree to:</p>"
                    "<ul>"
                    "<li>Provide accurate and complete information</li>"
                    "<li>Respond to communication in a timely manner</li>"
                    "<li>Supply all required content (text, images, credentials, etc.)</li>"
                    "<li>Ensure you have rights to any materials provided</li>"
                    "</ul>"
                    "<p>You must not:</p>"
                    "<ul>"
                    "<li>Use our services for illegal or harmful purposes</li>"
                    "<li>Attempt to exploit, hack, or disrupt our systems</li>"
                    "<li>Misrepresent your identity or intentions</li>"
                    "</ul>"
                    "<h2>6. Project Engagement and Workflow</h2>"
                    "<h3>6.1 Project Initiation</h3>"
                    "<p>Projects begin only after agreement and deposit payment.</p>"
                    "<h3>6.2 Communication</h3>"
                    "<p>Clients must maintain clear and timely communication. Delays from the client may affect delivery timelines.</p>"
                    "<h3>6.3 Delivery</h3>"
                    "<p>Delivery timelines are estimates and may vary depending on scope and revisions.</p>"
                    "<h2>7. Payment Terms</h2>"
                    "<ul>"
                    "<li>A 50% non-refundable deposit is required before project commencement</li>"
                    "<li>The remaining 50% must be paid before final delivery or deployment</li>"
                    "<li>Payments are accepted via agreed methods (e.g., M-Pesa, bank transfer, etc.)</li>"
                    "</ul>"
                    "<p>Failure to complete payment:</p>"
                    "<ul>"
                    "<li>May result in project suspension</li>"
                    "<li>May lead to withholding of final deliverables</li>"
                    "</ul>"
                    "<h2>8. Refund Policy</h2>"
                    "<ul>"
                    "<li>Deposits are non-refundable once work has commenced</li>"
                    "<li>Refunds (if any) are issued at the sole discretion of Bwire Global Tech</li>"
                    "<li>No refunds will be issued for completed or delivered work</li>"
                    "</ul>"
                    "<h2>9. Revisions and Scope Changes</h2>"
                    "<ul>"
                    "<li>Revisions are limited to the agreed project scope</li>"
                    "<li>Additional features or major changes will be billed separately</li>"
                    "<li>Continuous or excessive revisions may incur additional charges</li>"
                    "</ul>"
                    "<h2>10. Intellectual Property Rights</h2>"
                    "<h3>10.1 Ownership</h3>"
                    "<p>All work remains the property of Bwire Global Tech until full payment is received.</p>"
                    "<h3>10.2 Transfer of Rights</h3>"
                    "<p>Upon full payment, ownership of the final product is transferred to the client. Third-party tools, plugins, "
                    "or assets remain under their respective licenses.</p>"
                    "<h3>10.3 Portfolio Rights</h3>"
                    "<p>We reserve the right to showcase completed work in our portfolio and marketing materials.</p>"
                    "<h2>11. Third-Party Services</h2>"
                    "<p>We may integrate third-party services including:</p>"
                    "<ul>"
                    "<li>Hosting providers</li>"
                    "<li>Payment gateways (e.g., M-Pesa, PayPal)</li>"
                    "<li>APIs and external tools</li>"
                    "</ul>"
                    "<p>We are not responsible for:</p>"
                    "<ul>"
                    "<li>Downtime or failures of third-party services</li>"
                    "<li>Changes in third-party pricing or policies</li>"
                    "</ul>"
                    "<h2>12. Data and Security</h2>"
                    "<p>While we implement best practices for security, we do not guarantee absolute protection against cyber threats. "
                    "Clients are responsible for maintaining their own credentials and backups.</p>"
                    "<h2>13. Limitation of Liability</h2>"
                    "<p>To the maximum extent permitted by law, Bwire Global Tech shall not be liable for indirect, incidental, or "
                    "consequential damages, loss of revenue, data, or business opportunities, or service interruptions beyond our control.</p>"
                    "<h2>14. Indemnification</h2>"
                    "<p>You agree to indemnify and hold harmless Bwire Global Tech from any claims, damages, or liabilities arising from "
                    "your misuse of our services, content you provide, or violation of these Terms.</p>"
                    "<h2>15. Termination of Services</h2>"
                    "<p>We reserve the right to suspend or terminate services if:</p>"
                    "<ul>"
                    "<li>Terms are violated</li>"
                    "<li>Payments are not made</li>"
                    "<li>There is abuse, fraud, or unethical conduct</li>"
                    "</ul>"
                    "<h2>16. Governing Law</h2>"
                    "<p>These Terms shall be governed by and interpreted in accordance with the laws of Kenya.</p>"
                    "<h2>17. Changes to Terms</h2>"
                    "<p>We reserve the right to update these Terms at any time. Continued use of our services constitutes acceptance of the updated Terms.</p>"
                    "<h2>18. Contact Information</h2>"
                    "<p>For any inquiries regarding these Terms:<br>Bwire Global Tech<br>Email: bwireglobaltech917@gmail.com<br>Phone: 0722206805</p>"
            ),
        }
        terms_page, created = TermsPage.objects.get_or_create(pk=1, defaults=terms_defaults)
        if not created and not terms_page.body:
            TermsPage.objects.filter(pk=terms_page.pk).update(**terms_defaults)

        privacy_defaults = {
            "title": "Privacy Policy - Bwire Global Tech",
            "lede": (
                "This Privacy Policy explains how we collect, use, disclose, and safeguard your information when "
                "you visit our website or use our services."
            ),
            "body": (
                    "<h2>1. Introduction</h2>"
                    "<p>At Bwire Global Tech, we are committed to protecting your privacy and ensuring that your personal information "
                    "is handled in a safe and responsible manner. By using our website, you consent to the practices described in this policy.</p>"
                    "<h2>2. Information We Collect</h2>"
                    "<h3>2.1 Personal Information</h3>"
                    "<p>Information you voluntarily provide, including:</p>"
                    "<ul>"
                    "<li>Full name</li>"
                    "<li>Email address</li>"
                    "<li>Phone number</li>"
                    "<li>Project details and requirements</li>"
                    "</ul>"
                    "<h3>2.2 Technical Information</h3>"
                    "<p>Automatically collected data such as:</p>"
                    "<ul>"
                    "<li>IP address</li>"
                    "<li>Browser type and version</li>"
                    "<li>Device information</li>"
                    "<li>Pages visited and time spent on the website</li>"
                    "</ul>"
                    "<h3>2.3 Cookies and Tracking Technologies</h3>"
                    "<p>We may use cookies and similar technologies to:</p>"
                    "<ul>"
                    "<li>Enhance user experience</li>"
                    "<li>Analyze website traffic</li>"
                    "<li>Improve our services</li>"
                    "</ul>"
                    "<p>You can disable cookies through your browser settings.</p>"
                    "<h2>3. How We Use Your Information</h2>"
                    "<ul>"
                    "<li>Respond to inquiries and project requests</li>"
                    "<li>Provide and manage our services</li>"
                    "<li>Communicate with you regarding your project</li>"
                    "<li>Improve website functionality and performance</li>"
                    "<li>Analyze user behavior for better service delivery</li>"
                    "</ul>"
                    "<h2>4. Sharing of Information</h2>"
                    "<p>We do not sell, rent, or trade your personal information. We may share information with:</p>"
                    "<ul>"
                    "<li>Trusted third-party service providers (hosting, analytics, payment systems)</li>"
                    "<li>Legal authorities if required by law</li>"
                    "<li>Partners involved in delivering your project (only when necessary)</li>"
                    "</ul>"
                    "<h2>5. Data Security</h2>"
                    "<p>We implement appropriate technical and organizational measures to protect your data, including secure servers and hosting "
                    "environments, encryption where applicable, and restricted access to sensitive data.</p>"
                    "<p>However, no system is 100% secure, and we cannot guarantee absolute security.</p>"
                    "<h2>6. Data Retention</h2>"
                    "<p>We retain your personal information only as long as necessary to:</p>"
                    "<ul>"
                    "<li>Provide services</li>"
                    "<li>Comply with legal obligations</li>"
                    "<li>Resolve disputes</li>"
                    "</ul>"
                    "<h2>7. Your Rights</h2>"
                    "<p>Depending on your location, you may have the right to:</p>"
                    "<ul>"
                    "<li>Access your personal data</li>"
                    "<li>Request correction of inaccurate information</li>"
                    "<li>Request deletion of your data</li>"
                    "<li>Withdraw consent at any time</li>"
                    "</ul>"
                    "<p>To exercise these rights, contact us using the details below.</p>"
                    "<h2>8. Third-Party Links</h2>"
                    "<p>Our website may contain links to external websites. We are not responsible for the privacy practices or content of those third-party sites.</p>"
                    "<h2>9. Children's Privacy</h2>"
                    "<p>Our services are not intended for individuals under the age of 18. We do not knowingly collect personal data from children.</p>"
                    "<h2>10. International Data Transfers</h2>"
                    "<p>If you access our website from outside Kenya, your data may be transferred and processed in Kenya or other jurisdictions.</p>"
                    "<h2>11. Updates to This Privacy Policy</h2>"
                    "<p>We may update this Privacy Policy from time to time. Changes will be posted on this page with an updated revision date.</p>"
                    "<h2>12. Contact Information</h2>"
                    "<p>If you have any questions about this Privacy Policy or how your data is handled, contact us:<br>Bwire Global Tech<br>Email: "
                    "bwireglobaltech917@gmail.com<br>Phone: 0722206805</p>"
                    "<h2>Why this is strong</h2>"
                    "<ul>"
                    "<li>Covers legal, technical, and user trust requirements</li>"
                    "<li>Protects the company from liability</li>"
                    "<li>Builds confidence for clients (especially paying ones)</li>"
                    "<li>Works for web, AI, and data projects</li>"
                    "</ul>"
            ),
        }
        privacy_page, created = PrivacyPage.objects.get_or_create(pk=1, defaults=privacy_defaults)
        if not created and not privacy_page.body:
            PrivacyPage.objects.filter(pk=privacy_page.pk).update(**privacy_defaults)

        self.stdout.write(self.style.SUCCESS("CMS seed data ensured."))
