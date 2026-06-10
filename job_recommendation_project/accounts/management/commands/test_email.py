from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address to send test to')

    def handle(self, *args, **kwargs):
        recipient = kwargs['email']
        self.stdout.write(f'\nTesting email...')
        self.stdout.write(f'Backend: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'Gmail: {settings.EMAIL_HOST_USER or "NOT SET - check .env file"}')

        try:
            send_mail(
                subject='NexaJobs Email Test',
                message='Your email setup is working!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Email sent to {recipient}! Check inbox and spam.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Email failed: {e}'))
            self.stdout.write('Fix: Check .env file has correct Gmail and App Password')
