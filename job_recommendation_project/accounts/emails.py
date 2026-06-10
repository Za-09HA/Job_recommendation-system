"""
NexaJobs Email Notification System
=====================================
Sends emails for:
  - Welcome / registration
  - New job match alert (daily digest)
  - Application confirmation
  - Profile completion reminder

To use real Gmail:
  1. Enable 2FA on your Google account
  2. Create an App Password at myaccount.google.com/apppasswords
  3. Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py
  4. Change EMAIL_BACKEND to 'django.core.mail.backends.smtp.EmailBackend'
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def _send(subject, html_body, recipient_email, from_email=None):
    """Base helper — sends HTML email with plain-text fallback."""
    from_addr = from_email or settings.DEFAULT_FROM_EMAIL
    plain = strip_tags(html_body)
    msg = EmailMultiAlternatives(subject, plain, from_addr, [recipient_email])
    msg.attach_alternative(html_body, "text/html")
    try:
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"[NexaJobs Email] Failed to send to {recipient_email}: {e}")
        return False


def send_welcome_email(user):
    """Sent immediately after registration."""
    subject = f"Welcome to NexaJobs, {user.first_name or user.username}! 🎉"
    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,#4f8ef7,#7c3aed);padding:2rem;text-align:center;">
        <h1 style="margin:0;font-size:2rem;color:#fff;">⬡ NexaJobs</h1>
        <p style="color:rgba(255,255,255,.8);margin:.5rem 0 0;">AI-Powered Job Recommendations</p>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:#4f8ef7;">Welcome aboard, {user.first_name or user.username}!</h2>
        <p style="color:#8899b0;line-height:1.7;">
          Your account is all set. Here's how to get the most out of NexaJobs:
        </p>
        <ol style="color:#8899b0;line-height:2;">
          <li>✏️ <strong style="color:#e8edf5;">Complete your profile</strong> — add your skills and preferred roles</li>
          <li>🤖 <strong style="color:#e8edf5;">Get AI recommendations</strong> — see jobs matched to your profile</li>
          <li>💾 <strong style="color:#e8edf5;">Save & apply</strong> — track everything from your dashboard</li>
        </ol>
        <div style="text-align:center;margin:2rem 0;">
          <a href="{settings.FRONTEND_URL}/accounts/profile/edit/"
             style="background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            Complete Your Profile →
          </a>
        </div>
        <p style="color:#4a5a72;font-size:.85rem;text-align:center;">
          You're receiving this because you just registered at NexaJobs.
        </p>
      </div>
    </div>
    """
    _send(subject, html, user.email)


def send_job_match_alert(user, matched_jobs):
    """Sent when new jobs matching the user's profile are found."""
    if not matched_jobs:
        return
    count = len(matched_jobs)
    subject = f"🎯 {count} new job{'s' if count > 1 else ''} match your profile — NexaJobs"

    jobs_html = ""
    for job, score in matched_jobs[:5]:
        jobs_html += f"""
        <div style="background:#0a1628;border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:1.2rem;margin-bottom:.8rem;">
          <div style="font-weight:600;color:#e8edf5;font-size:1rem;">{job.title}</div>
          <div style="color:#8899b0;font-size:.85rem;margin:.3rem 0;">{job.company} &bull; {job.location}</div>
          <div style="color:#06d6a0;font-size:.85rem;font-weight:600;">{score}% match</div>
          <a href="{settings.FRONTEND_URL}/jobs/{job.pk}/"
             style="display:inline-block;margin-top:.8rem;background:rgba(79,142,247,.2);color:#4f8ef7;padding:.4rem 1rem;border-radius:50px;font-size:.82rem;text-decoration:none;">
            View Job →
          </a>
        </div>
        """

    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,#4f8ef7,#7c3aed);padding:1.5rem;text-align:center;">
        <h1 style="margin:0;font-size:1.5rem;color:#fff;">⬡ NexaJobs — New Matches</h1>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:#4f8ef7;">Hi {user.first_name or user.username}, {count} new job{'s match' if count > 1 else ' matches'} your profile!</h2>
        <p style="color:#8899b0;">Our AI found these opportunities based on your skills and preferences:</p>
        {jobs_html}
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/recommendations/"
             style="background:linear-gradient(135deg,#4f8ef7,#7c3aed);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            See All Recommendations →
          </a>
        </div>
      </div>
    </div>
    """
    _send(subject, html, user.email)


def send_application_confirmation(user, job):
    """Sent when a user marks a job as 'applied'."""
    subject = f"✅ Application recorded — {job.title} at {job.company}"
    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,#06d6a0,#00b386);padding:1.5rem;text-align:center;">
        <h1 style="margin:0;font-size:1.5rem;color:#fff;">✓ Application Recorded</h1>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:#06d6a0;">Great move, {user.first_name or user.username}!</h2>
        <p style="color:#8899b0;line-height:1.7;">
          We've noted that you applied for:
        </p>
        <div style="background:#0a1628;border:1px solid rgba(6,214,160,.2);border-radius:10px;padding:1.5rem;margin:1rem 0;">
          <div style="font-size:1.2rem;font-weight:700;color:#e8edf5;">{job.title}</div>
          <div style="color:#8899b0;margin:.4rem 0;">{job.company} &bull; {job.location}</div>
          <div style="color:#8899b0;font-size:.85rem;">{job.get_job_type_display()} &bull; {job.salary_display()}</div>
        </div>
        <p style="color:#8899b0;line-height:1.7;">
          Track all your applications in your dashboard. Good luck! 🚀
        </p>
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/feedback/saved/"
             style="background:linear-gradient(135deg,#06d6a0,#00b386);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            View My Applications →
          </a>
        </div>
      </div>
    </div>
    """
    _send(subject, html, user.email)


def send_profile_reminder(user):
    """Nudge incomplete profiles to add their skills."""
    subject = "💡 You're missing out on job matches — complete your NexaJobs profile"
    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,#fbbf24,#f59e0b);padding:1.5rem;text-align:center;">
        <h1 style="margin:0;font-size:1.5rem;color:#fff;">⚠ Profile Incomplete</h1>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:#fbbf24;">Hey {user.first_name or user.username}, your profile needs skills!</h2>
        <p style="color:#8899b0;line-height:1.7;">
          Without skills in your profile, our AI can't match you to the right jobs.
          It only takes 2 minutes to add them.
        </p>
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/accounts/profile/edit/"
             style="background:linear-gradient(135deg,#fbbf24,#f59e0b);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            Complete Profile Now →
          </a>
        </div>
      </div>
    </div>
    """
    _send(subject, html, user.email)


def send_application_status_email(user, job, status):
    """Sent when recruiter accepts or rejects an application."""
    if status == 'hired':
        subject = f"🎉 Congratulations! Your application for {job.title} has been accepted!"
        color = "#06d6a0"
        icon = "🎉"
        heading = f"Congratulations, {user.first_name or user.username}!"
        message = f"""
        <p style="color:#8899b0;line-height:1.7;">
            We are thrilled to inform you that your application for <strong style="color:#e8edf5;">{job.title}</strong>
            at <strong style="color:#e8edf5;">{job.company}</strong> has been <strong style="color:#06d6a0;">accepted!</strong>
        </p>
        <p style="color:#8899b0;line-height:1.7;">
            The hiring team will contact you shortly with next steps. Congratulations on this achievement!
        </p>
        """
    elif status == 'shortlisted':
        subject = f"📋 You've been shortlisted for {job.title} at {job.company}"
        color = "#4f8ef7"
        icon = "📋"
        heading = f"Great news, {user.first_name or user.username}!"
        message = f"""
        <p style="color:#8899b0;line-height:1.7;">
            You have been <strong style="color:#4f8ef7;">shortlisted</strong> for the position of
            <strong style="color:#e8edf5;">{job.title}</strong> at <strong style="color:#e8edf5;">{job.company}</strong>.
        </p>
        <p style="color:#8899b0;line-height:1.7;">
            The hiring team will be in touch with you soon regarding the next steps in the interview process.
        </p>
        """
    else:
        subject = f"Update on your application for {job.title} at {job.company}"
        color = "#f87171"
        icon = "📩"
        heading = f"Application Update, {user.first_name or user.username}"
        message = f"""
        <p style="color:#8899b0;line-height:1.7;">
            Thank you for your interest in the <strong style="color:#e8edf5;">{job.title}</strong>
            position at <strong style="color:#e8edf5;">{job.company}</strong>.
        </p>
        <p style="color:#8899b0;line-height:1.7;">
            After careful consideration, we regret to inform you that we have decided to move forward
            with other candidates at this time. We encourage you to keep applying and wish you the best!
        </p>
        """

    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,{color},{color}99);padding:1.5rem;text-align:center;">
        <h1 style="margin:0;font-size:1.5rem;color:#fff;">{icon} NexaJobs — Application Update</h1>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:{color};">{heading}</h2>
        {message}
        <div style="background:#0a1628;border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:1.2rem;margin:1rem 0;">
          <div style="font-weight:600;color:#e8edf5;">{job.title}</div>
          <div style="color:#8899b0;font-size:.85rem;margin:.3rem 0;">{job.company} &bull; {job.location}</div>
        </div>
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/feedback/my-applications/"
             style="background:linear-gradient(135deg,{color},{color}99);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            View My Applications →
          </a>
        </div>
      </div>
    </div>
    """
    _send(subject, html, user.email)


def send_message_notification(recipient, sender, job, message_text):
    """Notify user they received a message about their application."""
    subject = f"💬 New message about your application — {job.title}"
    color = "#4f8ef7"
    html = f"""
    <div style="font-family:sans-serif;max-width:560px;margin:0 auto;background:#050b18;color:#e8edf5;border-radius:12px;overflow:hidden;">
      <div style="background:linear-gradient(135deg,{color},{color}99);padding:1.5rem;text-align:center;">
        <h1 style="margin:0;font-size:1.5rem;color:#fff;">💬 New Message — NexaJobs</h1>
      </div>
      <div style="padding:2rem;">
        <h2 style="color:{color};">Hi {recipient.first_name or recipient.username}!</h2>
        <p style="color:#8899b0;line-height:1.7;">
          You have a new message from <strong style="color:#e8edf5;">{sender.first_name or sender.username}</strong>
          regarding the position of <strong style="color:#e8edf5;">{job.title}</strong> at
          <strong style="color:#e8edf5;">{job.company}</strong>.
        </p>
        <div style="background:#0a1628;border:1px solid rgba(79,142,247,.2);border-radius:10px;padding:1.2rem;margin:1rem 0;">
          <div style="color:#8899b0;font-size:.85rem;margin-bottom:.5rem;">Message:</div>
          <div style="color:#e8edf5;line-height:1.7;">{message_text}</div>
        </div>
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/feedback/my-applications/"
             style="background:linear-gradient(135deg,{color},{color}99);color:#fff;padding:.9rem 2rem;border-radius:50px;text-decoration:none;font-weight:600;">
            View Application →
          </a>
        </div>
      </div>
    </div>
    """
    _send(subject, html, recipient.email)


def send_hiring_greeting_email(user, job, recruiter_profile):
    """
    Sent automatically when recruiter clicks Accept (status=hired).
    Sends a professional greeting from the company inviting the applicant for an interview.
    """
    company = job.company
    recruiter_name = (
        recruiter_profile.user.get_full_name()
        or recruiter_profile.user.username
    )

    subject = f"Congratulations! You Have Been Selected — {job.title} | {company}"

    html = f"""
    <div style="font-family:sans-serif;max-width:600px;margin:0 auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e5e7eb;">

      <!-- Header -->
      <div style="background:#0f1b2d;padding:2rem;text-align:center;">
        <h1 style="margin:0;font-size:1.8rem;color:#ffffff;font-weight:700;">{company}</h1>
        <p style="color:#93c5fd;margin:.5rem 0 0;font-size:.95rem;">Human Resources Department</p>
      </div>

      <!-- Accent bar -->
      <div style="height:4px;background:linear-gradient(90deg,#2563eb,#7c3aed);"></div>

      <!-- Body -->
      <div style="padding:2.5rem;">

        <p style="color:#6b7280;font-size:.9rem;margin:0 0 1.5rem;">Dear {user.first_name or user.username} {user.last_name or ''},</p>

        <h2 style="color:#0f1b2d;font-size:1.3rem;margin:0 0 1rem;">
          Congratulations! You Have Been Selected 🎉
        </h2>

        <p style="color:#374151;line-height:1.8;margin:0 0 1rem;">
          We are delighted to inform you that after a thorough review of your application
          and qualifications, the hiring team at <strong>{company}</strong> has decided
          to move forward with your candidacy for the position of:
        </p>

        <!-- Job box -->
        <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;padding:1.2rem;margin:1.2rem 0;">
          <div style="font-size:1.1rem;font-weight:700;color:#1e40af;">{job.title}</div>
          <div style="color:#6b7280;font-size:.9rem;margin:.3rem 0;">{company} &bull; {job.location}</div>
          <div style="color:#6b7280;font-size:.85rem;">{job.get_job_type_display()}</div>
        </div>

        <p style="color:#374151;line-height:1.8;margin:0 0 1.5rem;">
          Your impressive background and skills stood out to us and we are excited
          about the possibility of you joining our team!
        </p>

        <!-- Interview section -->
        <div style="background:#f9fafb;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:1.2rem 1.5rem;margin:1.5rem 0;">
          <h3 style="color:#1e40af;margin:0 0 .8rem;font-size:1rem;">Interview Invitation</h3>
          <p style="color:#374151;line-height:1.8;margin:0 0 .8rem;">
            We would like to invite you for an interview at your earliest convenience.
            The details are as follows:
          </p>
          <table style="color:#374151;font-size:.9rem;line-height:2;">
            <tr><td style="padding-right:1rem;">&#128197; <strong>Date:</strong></td><td>To be confirmed upon your availability</td></tr>
            <tr><td style="padding-right:1rem;">&#128336; <strong>Time:</strong></td><td>11:00 AM – 12:00 PM (PKT)</td></tr>
            <tr><td style="padding-right:1rem;">&#128205; <strong>Location:</strong></td><td>{company} Office, Lahore, Pakistan (or Google Meet)</td></tr>
            <tr><td style="padding-right:1rem;">&#128100; <strong>Interviewer:</strong></td><td>HR Team &amp; Hiring Manager</td></tr>
          </table>
        </div>

        <!-- Interview rounds -->
        <h3 style="color:#0f1b2d;font-size:1rem;margin:1.5rem 0 .8rem;">Interview Process</h3>
        <div style="background:#f9fafb;border-radius:8px;padding:1.2rem;">
          <div style="display:flex;margin-bottom:.8rem;">
            <div style="background:#2563eb;color:#fff;border-radius:50%;width:24px;height:24px;text-align:center;line-height:24px;font-size:.8rem;font-weight:700;flex-shrink:0;margin-right:.8rem;">1</div>
            <div>
              <strong style="color:#1e40af;">HR Round</strong> (30 minutes)<br>
              <span style="color:#6b7280;font-size:.85rem;">Cultural fit, background, and career goals</span>
            </div>
          </div>
          <div style="display:flex;">
            <div style="background:#7c3aed;color:#fff;border-radius:50%;width:24px;height:24px;text-align:center;line-height:24px;font-size:.8rem;font-weight:700;flex-shrink:0;margin-right:.8rem;">2</div>
            <div>
              <strong style="color:#6d28d9;">Technical Round</strong> (45 minutes)<br>
              <span style="color:#6b7280;font-size:.85rem;">Role-specific technical questions and problem solving</span>
            </div>
          </div>
        </div>

        <p style="color:#374151;line-height:1.8;margin:1.5rem 0;">
          Please reply to this email to confirm your availability or suggest an
          alternative date and time that works best for you. We are happy to accommodate
          your schedule.
        </p>

        <p style="color:#374151;line-height:1.8;margin:0 0 2rem;">
          We look forward to welcoming you to the <strong>{company}</strong> family!
        </p>

        <!-- CTA -->
        <div style="text-align:center;margin:1.5rem 0;">
          <a href="{settings.FRONTEND_URL}/feedback/my-applications/"
             style="background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;padding:1rem 2.5rem;border-radius:50px;text-decoration:none;font-weight:600;font-size:1rem;display:inline-block;">
            View My Application Status →
          </a>
        </div>

        <hr style="border:none;border-top:1px solid #e5e7eb;margin:2rem 0;">

        <p style="color:#374151;margin:0 0 .3rem;">Warm regards,</p>
        <p style="color:#0f1b2d;font-weight:700;margin:0;">{recruiter_name}</p>
        <p style="color:#6b7280;font-size:.85rem;margin:.2rem 0;">HR Department — {company}</p>
      </div>

      <!-- Footer -->
      <div style="background:#f3f4f6;padding:1rem;text-align:center;">
        <p style="color:#9ca3af;font-size:.8rem;margin:0;">
          This email was sent via NexaJobs &bull; {settings.FRONTEND_URL}
        </p>
      </div>
    </div>
    """
    _send(subject, html, user.email)
