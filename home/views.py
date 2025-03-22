from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ResidentProfile
from .models import Message, Notification


# ✅ Import models correctly
from .models import CaregiverProfile, CustomUser, ResidentProfile  
from .forms import UserSignupForm, CaregiverSignupForm, ResidentProfileForm  

def home(request):
    return render(request, "index.html", {"media_url": settings.MEDIA_URL})

# ✅ User Signup
def user_signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("resident_dashboard")
        else:
            messages.error(request, "Error in form submission.")
    else:
        form = UserSignupForm()
    return render(request, "user_signup.html", {"form": form})

# ✅ User Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.is_active:
                login(request, user)
                return redirect("resident_dashboard")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid login details.")
    
    form = AuthenticationForm()
    return render(request, "user_login.html", {"form": form})

# ✅ Caregiver Signup
def caregiver_signup(request):
    if request.method == "POST":
        form = CaregiverSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # ✅ Split full_name into first_name & last_name
            full_name = form.cleaned_data["full_name"]
            name_parts = full_name.split(" ", 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""

            user.user_type = "caregiver"
            user.save()

            # ✅ Create Caregiver Profile
            CaregiverProfile.objects.create(
                user=user,
                experience=form.cleaned_data["experience"],
                qualifications=form.cleaned_data["qualifications"],
                availability=form.cleaned_data["availability"],
                location=form.cleaned_data["location"],
            )

            messages.success(request, "Caregiver account created successfully!")
            return redirect("care_giver")

    else:
        form = CaregiverSignupForm()

    return render(request, "caregiversignup.html", {"form": form})

# ✅ Caregiver Login
def caregiver_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user and user.is_active:
                if user.user_type == "caregiver":
                    login(request, user)
                    return redirect("caregiver_dashboard")
                else:
                    messages.error(request, "You are not registered as a caregiver.")
            else:
                messages.error(request, "Invalid caregiver credentials.")
        else:
            messages.error(request, "Invalid login details.")

    form = AuthenticationForm()
    return render(request, "care_giver.html", {"form": form})

# ✅ Logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

def care_giver(request):
    return render(request, "care_giver.html")

@login_required
def healthcare_status(request):
    return render(request, "healthcare_status.html")

@login_required
def message_dashboard(request):
    return render(request, "message_dashboard.html")

# ✅ Resident Profile Form (Fixed version)
@login_required
def resident_profile(request):
    resident, created = ResidentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        print("Received POST data:", request.POST)  # Debugging line
        form = ResidentProfileForm(request.POST, request.FILES, instance=resident)
        
        if form.is_valid():
            form.save()
            print("Form saved successfully!")  # Debugging line
            return redirect("resident_dashboard")
        else:
            print("Form errors:", form.errors)  # Debugging line

    else:
        form = ResidentProfileForm(instance=resident)

    return render(request, "resident_profile.html", {"form": form, "resident": resident})


# ✅ Resident Dashboard
from django.shortcuts import render
from django.utils.timezone import now
from .models import ResidentProfile

def resident_dashboard(request):
    user = request.user
    resident = ResidentProfile.objects.get(user=user)

    # Fetch reminder details
    reminder_time = resident.reminder_time
    reminder_message = resident.reminder_message

    context = {
        "resident": resident,
        "reminder_time": reminder_time,
        "reminder_message": reminder_message,
        "current_time": now().time(),  # Pass the current time for comparison
    }

    return render(request, "resident_user_dashboard.html", context)

# ✅ Caregiver Dashboard
@login_required
def caregiver_dashboard(request):
    return render(request, "caregiver_dashboard.html")

@login_required
def update_health_status(request):
    resident = get_object_or_404(ResidentProfile, user=request.user)

    if request.method == "POST":
        selected_conditions = request.POST.getlist("conditions")  # Get list of selected checkboxes
        resident.conditions = ",".join(selected_conditions)  # Store as CSV (comma-separated string)

        resident.allergies = request.POST.get("allergies", "")
        resident.medications = request.POST.get("medications", "")
        resident.medication_schedule = request.POST.get("medication_schedule", "")
        resident.doctor_name = request.POST.get("doctor_name", "")
        resident.doctor_phone = request.POST.get("doctor_phone", "")
        resident.reminder_time = request.POST.get("reminder_time", None)

        resident.save()
        return redirect("resident_dashboard")

    # ✅ Process the string **inside the view**, NOT in the template
    conditions_set = set(resident.conditions.split(",")) if resident.conditions else set()

    return render(request, "healthcare_status.html", {"resident": resident, "conditions_set": conditions_set})
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Message  # Import your Message model
@csrf_exempt
def delete_message(request, message_id):
    if request.method == "POST":
        try:
            message = Message.objects.get(id=message_id, user=request.user)
            message.delete()
            return JsonResponse({"success": True})
        except Message.DoesNotExist:
            return JsonResponse({"success": False, "error": "Message not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
@login_required
def message_dashboard(request):
    messages = Message.objects.filter(user=request.user)  # Fetch messages for the logged-in user
    return render(request, "message_dashboard.html", {"messages": messages})

@login_required
def notification_dashboard(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "notification_dashboard.html", {"notifications": notifications})

# Mark Notification as Read
@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect("notification_dashboard")

# Send a New Message and Create Notification
@login_required
def send_message(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        # Create Message
        message = Message.objects.create(user=request.user, title=title, content=content)

        # Create Notification for the same user
        Notification.objects.create(
            user=request.user,  # You can send to another user if needed
            title="New Message",
            message=f"You have a new message: {title}",
        )

        return redirect("message_dashboard")
    return render(request, "send_message.html")