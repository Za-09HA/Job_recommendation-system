from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, ProfileForm
from .models import UserProfile
from .emails import send_welcome_email


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_recruiter = request.POST.get('is_recruiter', 'false') == 'true'
            company_name = form.cleaned_data.get('company_name', '')
            profile = UserProfile.objects.create(
                user=user,
                is_recruiter=is_recruiter,
                company_name=company_name
            )
            login(request, user)
            try:
                send_welcome_email(user)
            except Exception:
                pass
            if is_recruiter:
                messages.success(request, f'Welcome {user.first_name}! Your recruiter account is ready.')
                return redirect('recruiter_dashboard')
            else:
                messages.success(request, f'Welcome {user.first_name}! Complete your profile for better recommendations.')
                return redirect('profile_edit')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Always redirect based on role
            try:
                profile = user.profile
                if profile.is_recruiter:
                    return redirect('recruiter_dashboard')
            except Exception:
                pass
            next_url = request.GET.get('next', '')
            if next_url and 'recruiter' not in next_url:
                return redirect(next_url)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            prof = form.save(commit=False)
            if 'resume_pdf' in request.FILES:
                prof.save()
                extracted = prof.extract_resume_text()
                prof.resume_text = extracted
                if extracted:
                    messages.success(request, f'Resume uploaded and parsed successfully.')
                else:
                    messages.warning(request, 'Resume uploaded but text could not be extracted.')
            prof.save()
            messages.success(request, 'Profile updated!')
            if profile.is_recruiter:
                return redirect('recruiter_dashboard')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form, 'profile': profile})
