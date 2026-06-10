from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_recruiter = forms.BooleanField(required=False, label='Register as Recruiter')
    company_name = forms.CharField(max_length=200, required=False, label='Company Name')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2','is_recruiter','company_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','skills','experience_level','experience_years',
                  'preferred_roles','preferred_location','resume_pdf',
                  'avatar','linkedin_url','github_url','company_name','company_description']
        widgets = {
            'bio': forms.Textarea(attrs={'rows':3,'class':'form-control','placeholder':'Tell us about yourself...'}),
            'skills': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Python, Django, React, SQL'}),
            'experience_level': forms.Select(attrs={'class':'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class':'form-control','min':0,'max':50}),
            'preferred_roles': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Backend Developer, Data Scientist'}),
            'preferred_location': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Remote, Lahore, Karachi'}),
            'linkedin_url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://linkedin.com/in/yourname'}),
            'github_url': forms.URLInput(attrs={'class':'form-control','placeholder':'https://github.com/yourname'}),
            'company_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Your Company Name'}),
            'company_description': forms.Textarea(attrs={'rows':3,'class':'form-control','placeholder':'Describe your company...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume_pdf'].widget.attrs.update({'class': 'form-control', 'accept': '.pdf'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'accept': 'image/*'})

    def clean_resume_pdf(self):
        f = self.cleaned_data.get('resume_pdf')
        if f and hasattr(f, 'name'):
            if not f.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            if f.size > 5 * 1024 * 1024:
                raise forms.ValidationError('PDF file size must be under 5MB.')
        return f
