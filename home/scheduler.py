from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from django.utils.timezone import now
from .models import ResidentProfile
from django.core.mail import send_mail

def send_medication_reminder():
    """Function to check medication times and send reminders"""
    current_time = now().strftime("%H:%M")  # Get current time in HH:MM format
    residents = ResidentProfile.objects.filter(reminder_time=current_time)

    for resident in residents:
        message = f"Hello {resident.user.username}, it's time to take your medication!"
        
        # Send Email Reminder (optional)
        send_mail(
            subject="Medication Reminder",
            message=message,
            from_email="your_email@example.com",  # Replace with your email
            recipient_list=[resident.user.email],
            fail_silently=True,
        )
        
        print(f"Reminder sent to {resident.user.username} at {current_time}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_medication_reminder, "interval", minutes=1)  # Runs every 1 minute
    scheduler.start()
