# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import ResidentProfile
from datetime import datetime

@shared_task
def send_medication_reminder():
    # Get all residents who need a medication reminder
    residents = ResidentProfile.objects.filter(reminder_time__lt=datetime.now())
    
    for resident in residents:
        # Send reminder email or notification (example)
        send_mail(
            'Medication Reminder',
            resident.reminder_message,
            'from@example.com',  # Sender email
            [resident.user.email],
            fail_silently=False,
        )
        print(f"Reminder sent to {resident.user.email}")
