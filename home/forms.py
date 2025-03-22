from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ResidentProfile, CustomUser, CaregiverProfile

class UserSignupForm(UserCreationForm):
    full_name = forms.CharField(required=True, max_length=100)

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "email", "password1", "password2"]

class CaregiverSignupForm(UserCreationForm):
    full_name = forms.CharField(required=True, max_length=100)
    experience = forms.IntegerField(required=True, min_value=0)
    qualifications = forms.CharField(required=False, max_length=255)
    availability = forms.CharField(required=False, max_length=255)
    location = forms.CharField(required=False, max_length=255)

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data["full_name"]
        user.user_type = "caregiver"

        if commit:
            user.save()
            CaregiverProfile.objects.create(
                user=user,
                experience=self.cleaned_data["experience"],
                qualifications=self.cleaned_data["qualifications"],
                availability=self.cleaned_data["availability"],
                location=self.cleaned_data["location"],
            )
        return user

class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = ResidentProfile
        fields = [
            "name", "age", "gender", "room", "phone", "photo", "meal", "assistance", "visit_schedule",
            "emergency_contact", "emergency_phone", "conditions", "allergies", "medications",
            "medication_schedule", "doctor_name", "doctor_phone", "reminder_time"
        ]