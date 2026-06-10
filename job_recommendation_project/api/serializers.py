from rest_framework import serializers
from django.contrib.auth.models import User
from jobs.models import JobListing
from accounts.models import UserProfile
from feedback.models import UserFeedback
from recommendations.engine import get_match_percentage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills_list = serializers.SerializerMethodField()
    preferred_roles_list = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'skills', 'skills_list', 'experience_level',
                  'experience_years', 'preferred_roles', 'preferred_roles_list',
                  'preferred_location', 'linkedin_url', 'github_url', 'created_at']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_preferred_roles_list(self, obj):
        return obj.get_preferred_roles_list()


class JobListingSerializer(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField()
    salary_display = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    job_type_display = serializers.CharField(source='get_job_type_display', read_only=True)
    experience_display = serializers.CharField(source='get_experience_required_display', read_only=True)
    match_percent = serializers.SerializerMethodField()

    class Meta:
        model = JobListing
        fields = ['id', 'title', 'company', 'description', 'required_skills', 'skills_list',
                  'location', 'job_type', 'job_type_display', 'category', 'category_display',
                  'experience_required', 'experience_display', 'salary_min', 'salary_max',
                  'salary_display', 'source_url', 'is_active', 'posted_at', 'match_percent']

    def get_skills_list(self, obj):
        return obj.get_skills_list()

    def get_salary_display(self, obj):
        return obj.salary_display()

    def get_match_percent(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                profile = request.user.profile
                return get_match_percentage(profile, obj)
            except Exception:
                return None
        return None


class FeedbackSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_company = serializers.CharField(source='job.company', read_only=True)

    class Meta:
        model = UserFeedback
        fields = ['id', 'job', 'job_title', 'job_company', 'action', 'created_at']
        read_only_fields = ['created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user
