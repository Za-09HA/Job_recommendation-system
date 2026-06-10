from django import forms
from jobs.models import JobListing, JOB_TYPE_CHOICES, CATEGORY_CHOICES, EXPERIENCE_REQUIRED

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title','company','description','required_skills','location',
                  'job_type','category','experience_required','salary_min','salary_max','source_url']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Senior Python Developer'}),
            'company': forms.TextInput(attrs={'class':'form-control','placeholder':'Company name'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows':6,'placeholder':'Describe the role, responsibilities, requirements...'}),
            'required_skills': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Python, Django, SQL, React'}),
            'location': forms.TextInput(attrs={'class':'form-control','placeholder':'e.g. Lahore, Pakistan or Remote'}),
            'job_type': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'experience_required': forms.Select(attrs={'class':'form-control'}),
            'salary_min': forms.NumberInput(attrs={'class':'form-control','placeholder':'Min salary (PKR)'}),
            'salary_max': forms.NumberInput(attrs={'class':'form-control','placeholder':'Max salary (PKR)'}),
            'source_url': forms.URLInput(attrs={'class':'form-control','placeholder':'Job listing URL (optional)'}),
        }
