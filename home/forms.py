from django import forms


class ContactForm(forms.Form):
    full_name = forms.CharField(
        max_length=120, widget=forms.TextInput(attrs={"placeholder": "Your full name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"})
    )
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
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Tell us about your project"})
    )
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
    # Honeypot field to trap bots — should remain empty in real submissions
    hp_field = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_hp_field(self):
        val = self.cleaned_data.get("hp_field")
        if val:
            raise forms.ValidationError("Spam detected.")
        return val

    def clean_reference_file(self):
        f = self.cleaned_data.get("reference_file")
        if not f:
            return f
        # 2.5 MB limit (same as settings DATA_UPLOAD_MAX_MEMORY_SIZE)
        max_size = 2_621_440
        if f.size > max_size:
            raise forms.ValidationError("File too large (max 2.5MB).")
        # Basic content-type check (allow common document and image types)
        allowed = [
            "image/png",
            "image/jpeg",
            "image/jpg",
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
        ]
        content_type = getattr(f, "content_type", "")
        if content_type and content_type not in allowed:
            raise forms.ValidationError("Unsupported file type.")
        return f
