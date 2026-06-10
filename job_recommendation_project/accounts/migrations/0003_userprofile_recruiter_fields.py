from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_userprofile_resume_pdf_and_more'),
    ]
    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_recruiter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company_name',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='company_description',
            field=models.TextField(blank=True),
        ),
    ]
