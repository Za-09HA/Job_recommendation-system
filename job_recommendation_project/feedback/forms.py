from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'full_name','email','phone','cover_letter','resume_pdf',
            'portfolio_url','linkedin_url','years_of_experience',
            'current_company','expected_salary','notice_period',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Your full name'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'your@email.com'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder':'+1 234 567 8900'}),
            'cover_letter': forms.Textarea(attrs={'class':'form-control','rows':6,
                'placeholder':'Tell the employer why you are a great fit for this role...'}),
            'portfolio_url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://yourportfolio.com'}),
            'linkedin_url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://linkedin.com/in/yourname'}),
            'years_of_experience': forms.NumberInput(attrs={'class':'form-control','min':0,'max':50}),
            'current_company': forms.TextInput(attrs={'class':'form-control','placeholder':'Current or last company (optional)'}),
            'expected_salary': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. $60,000/year or Negotiable'}),
            'notice_period': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Immediate, 2 weeks, 1 month'}),
        }

    def __init__(self, *args, user=None, job=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume_pdf'].widget.attrs.update({'class':'form-control','accept':'.pdf'})
        self.fields['portfolio_url'].required = False
        self.fields['linkedin_url'].required = False
        self.fields['current_company'].required = False
        self.fields['expected_salary'].required = False
        self.fields['notice_period'].required = False
        # Pre-fill from user profile
        if user and hasattr(user, 'profile'):
            p = user.profile
            self.initial['full_name'] = user.get_full_name() or user.username
            self.initial['email'] = user.email
            self.initial['years_of_experience'] = p.experience_years
            self.initial['linkedin_url'] = p.linkedin_url
            if p.resume_pdf:
                self.fields['resume_pdf'].required = False
                self.fields['resume_pdf'].help_text = 'Leave blank to use your profile resume.'

    def clean_resume_pdf(self):
        f = self.cleaned_data.get('resume_pdf')
        if f and hasattr(f, 'name'):
            if not f.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError('PDF must be under 5MB.')
        return f
