from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("resident", "Resident"),
        ("caregiver", "Caregiver"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="resident")

class CaregiverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="caregiver_profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)  
    location = models.CharField(max_length=255, blank=True, null=True)  

    def __str__(self):
        return f"Caregiver Profile: {self.user.username}"

class ResidentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resident_profile")  # ✅ Corrected user field
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    room = models.CharField(max_length=10)
    phone = models.CharField(max_length=15, blank=True, null=True) 
    photo = models.ImageField(upload_to="resident_photos/", blank=True, null=True)
    meal = models.CharField(max_length=50, blank=True, null=True)
    assistance = models.CharField(max_length=100, blank=True, null=True)
    visit_schedule = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    emergency_phone = models.CharField(max_length=15, null=True, blank=True) 
    conditions = models.CharField(max_length=255, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    medication_schedule = models.CharField(max_length=50, blank=True, null=True)
    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    doctor_phone = models.CharField(max_length=15, blank=True, null=True)
    reminder_time = models.TimeField(blank=True, null=True)  # ✅ Corrected field
    reminder_message = models.TextField(default="Take the medicine")  # ✅ Default reminder message


    def __str__(self):
        return f"Resident Profile: {self.user.username}"
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ Correct reference
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
class Notification(models.Model):
    resident = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)