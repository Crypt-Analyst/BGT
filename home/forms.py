from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"placeholder": "Your full name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    phone = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={"placeholder": "Phone or WhatsApp"}),
    )
    project_type = forms.ChoiceField(
        choices=[
            ("starter", "Starter Website"),
            ("business", "Business Website"),
            ("premium", "Premium / E-commerce"),
            ("custom", "Custom Tech Solution"),
        ],
        widget=forms.Select(),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Tell us about your project"}))
    budget_range = forms.ChoiceField(
        required=False,
        choices=[
            ("", "Select a budget range"),
            ("under-30000", "Under Ksh 30,000"),
            ("30000-65000", "Ksh 30,000 - 65,000"),
            ("65000-120000", "Ksh 65,000 - 120,000"),
            ("120000-plus", "Ksh 120,000+"),
            ("not-sure", "Not sure yet"),
        ],
        widget=forms.Select(),
    )
    timeline = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Target deadline or launch date"}),
    )
    referral_source = forms.ChoiceField(
        required=False,
        choices=[
            ("", "How did you hear about us?"),
            ("referral", "Referral"),
            ("instagram", "Instagram"),
            ("tiktok", "TikTok"),
            ("google", "Google"),
            ("other", "Other"),
        ],
        widget=forms.Select(),
    )
    reference_file = forms.FileField(required=False)