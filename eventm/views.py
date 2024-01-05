from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
import base64, time
from .forms import LoginaForm, SignupForm, LoginuForm, ContactForm, EventForm, TicketPurchaseForm
from .models import ContactFormEntry, Event, UserEventRegistration
import face_recognition, os
import matplotlib
matplotlib.use('Agg')  # Use Agg backend (non-interactive) for Matplotlib
import matplotlib.pyplot as plt
from io import BytesIO

def check_facial_recognition(image_file):
    unknown_image = face_recognition.load_image_file(image_file)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    for i in os.listdir(r'images/admin'):
        image_path=os.path.join(r'images/admin',i)
        known_image = face_recognition.load_image_file(image_path)    
        known_encoding = face_recognition.face_encodings(known_image)[0]
        results = face_recognition.compare_faces([known_encoding], unknown_encoding)
        print(results)
        if results[0]:
            print(i)
            return True    
    
    return False

def convert_base64_to_image(base64_data):
    if base64_data is None:
         print("Error: Image data not found in the request.")
         return HttpResponse("Image data not found in the request.", status=400)

    # Remove the data URL prefix if it exists
    base64_data = base64_data.replace("data:image/png;base64,", "")

    if not base64_data:
        print("Error: Empty base64 data received.")
        return None

    try:
        # Decode the base64 string to bytes
        image_data = base64.b64decode(base64_data)
        # Set the path where you want to save the image
        path = "C:\\Users\\Hammad Yasin\\Event\\images\\"
        # Create a unique file name based on the current time
        file_name = str(time.time()) + ".png"
        # Write the image data to the file
        with open(os.path.join(path, file_name), "wb") as f:
            f.write(image_data)
        # Return the file name
        return file_name
    except Exception as e:
        print(f"Error during base64 decoding: {e}")
        return None

def index(request):
    return render(request, "eventm/index.html")

def add(request):
    success_message = None

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Associate the currently logged-in user with the event
            form.instance.user = request.user

            # Save the form data to the database
            event = form.save()
            UserEventRegistration.objects.create(user=request.user, event=event, status='pending')
            success_message = 'Event Request Successfully submitted!'
            form = EventForm()  # Reset the form for a new submission
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = EventForm()

    return render(request, "eventm/addevent.html", {'form': form, 'success_message': success_message})

def contact(request):
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            success_message = 'Thank you for your message! We will get back to you soon.'
            form = ContactForm()  # Reset the form for a new submission
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = ContactForm()

    return render(request, "eventm/contact_us.html", {'form': form, 'success_message': success_message})


def logina_view(request):
    if request.method == 'POST':
        form = LoginaForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # Get the base64 data from the form
            base64_data = request.POST.get('image')
            
            if base64_data is None:
                error_message = 'Image data not found in the request.'
                print("Error:", error_message)
                return JsonResponse({'success': False, 'error': error_message})

            path = "C:\\Users\\Hammad Yasin\\Event\\images\\"
            # Convert the base64 data to an image file and get the file name
            image_file = convert_base64_to_image(base64_data)
            image_path= os.path.join(path,image_file)
            if image_file is not None:
                if user is not None:
                    if check_facial_recognition(image_path):
                        login(request, user)
                        messages.success(request, 'Login successful.')
                        return redirect('dash_analytics')
                    else:
                        error_message = 'Facial recognition failed.'
                        print("Error:", error_message)
                        return JsonResponse({'success': False, 'error': error_message})
                else:
                    error_message = 'Invalid login credentials.'
                    print("Error:", error_message)
                    return JsonResponse({'success': False, 'error': error_message})
            else:
                error_message = 'Invalid image data.'
                print("Error:", error_message)
                return JsonResponse({'success': False, 'error': error_message})
    else:
        form = LoginaForm()

    return render(request, 'eventm/logina.html', {'form': form})

def dash_analytics(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to login if not authenticated
        return redirect('index')

    # Check if the session has expired
    if '_session_expiry' not in request.session:
        # Set the session expiry timestamp
        request.session['_session_expiry'] = int(time.mktime((timezone.now() + timezone.timedelta(minutes=15)).timetuple()))

    if int(request.session['_session_expiry']) < int(time.mktime(timezone.now().timetuple())):
        # Logout the user and redirect to the login page
        logout(request)
        messages.warning(request, 'Session expired. Please log in again.')
        return redirect('index')

    # Update the session expiry timestamp
    request.session['_session_expiry'] = int(time.mktime((timezone.now() + timezone.timedelta(minutes=15)).timetuple()))

    # Add the logic for generating charts
    category_labels = ['Conference', 'Workshop', 'Concerts', 'Weddings']
    category_counts = [30, 45, 20, 15]
    colors_categories = ['#333a55', '#4d5573', '#667190', '#7f8aae']

    # Create a bar chart for event categories
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(category_labels, category_counts, color=colors_categories)
    ax.set_xlabel('Event Categories')
    ax.set_ylabel('Number of Events')
    ax.set_title('Event Category')

    # Save the category chart to a BytesIO object
    category_stream = BytesIO()
    plt.savefig(category_stream, format='png')
    plt.close()

    # Pie chart for event status
    status_labels = ['Completed', 'Approved', 'Ongoing']
    status_counts = [60, 25, 15]
    colors_status = ['#7CAEA3', '#A4D4BE', '#CCE8D8']

    # Create a pie chart for event status
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(status_counts, labels=status_labels, autopct='%1.1f%%', colors=colors_status, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    ax.set_title('Event Status')

    # Save the status chart to a BytesIO object
    status_stream = BytesIO()
    plt.savefig(status_stream, format='png')
    plt.close()

    # Encode both image streams to base64
    category_base64 = base64.b64encode(category_stream.getvalue()).decode('utf-8')
    status_base64 = base64.b64encode(status_stream.getvalue()).decode('utf-8')

    # Pass the base64 image data to the template
    context = {
        'category_base64': category_base64,
        'status_base64': status_base64,
    }

    return render(request, "eventm/dash_analytics.html", context)

def logouta_view(request):
    logout(request)
    return redirect('index')

def signup_view(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            user = User.objects.create_user(username, email, password1)
            messages.success(request, 'Sign up successful. You can now log in.')
            # Redirect to a success page or any other desired page
            return redirect('loginu_view')
    else:
        form = SignupForm()

    return render(request, 'eventm/signup.html', {'form': form})
def loginu_view(request):
    form = LoginuForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('user_dashboard')  # Replace 'index' with your desired page
        else:
            # Invalid login credentials
            messages.error(request, 'Invalid login credentials.')
            
    # Render the login page
    return render(request, 'eventm/loginu.html',{'form': form}) 


def dash_contact(request):
    # Retrieve the contact form entries from the database
    contact_entries = ContactFormEntry.objects.all()

    context = {
        'contact_entries': contact_entries,
    }

    return render(request, "eventm/dash_contact.html", context)

def user_dashboard(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        return redirect('index')  # Redirect to the login page if the user is not authenticated

    # Fetch events that the user is registered for with an approved status
    user_registrations = UserEventRegistration.objects.filter(user=request.user)
    registered_event_ids = user_registrations.values_list('event__id', flat=True)
    registered_events = Event.objects.filter(id__in=registered_event_ids)

    # Fetch approved events excluding events of type 'Wedding'
    approved_events = Event.objects.filter(status='approved').exclude(id__in=registered_event_ids, event_type='Wedding')

    context = {
        'registered_events': registered_events,
        'approved_events': approved_events,
    }

    return render(request, "eventm/user_dashboard.html", context)

def all_events(request):
    all_events = Event.objects.all()
    print(all_events)
    context = {
        'all_events': all_events,
    }

    return render(request, 'eventm/pending_events.html', context)

def approved_events(request):
    # Filter events that are approved
    approved_events = Event.objects.filter(status='approved')
    context = {
        'approved_events': approved_events,
    }

    return render(request, 'eventm/approved_events.html', context)

def rejected_events(request):
    # Filter events that are rejected
    rejected_events = Event.objects.filter(status='rejected')
    print(rejected_events)
    context = {
        'rejected_events': rejected_events,
    }

    return render(request, 'eventm/rejected_events.html', context)
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Update the status of the event to 'approved'
    event.status = 'approved'
    event.save()

    # Update UserEventRegistration status to 'approved'
    user_registration = UserEventRegistration.objects.filter(event=event)
    user_registration.update(status='approved')

    messages.success(request, f'The event "{event.name}" has been approved.')
    return redirect('all_events')

def reject_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Update the status of the event to 'rejected'
    event.status = 'rejected'
    event.save()

    # Update UserEventRegistration status to 'rejected'
    user_registration = UserEventRegistration.objects.filter(event=event)
    user_registration.update(status='rejected')

    messages.success(request, f'The event "{event.name}" has been rejected.')
    return redirect('all_events')
from django.contrib import messages

def buy_tickets(request, event_id):
    event = Event.objects.get(pk=event_id)

    if not request.user.is_authenticated:
        return redirect('index')

    if event.status == 'approved' and not UserEventRegistration.objects.filter(user=request.user, event=event).exists():
        form = TicketPurchaseForm()

        if request.method == 'POST':
            form = TicketPurchaseForm(request.POST)
            if form.is_valid():
                # Associate the form data with the event and user
                ticket_purchase = form.save(commit=False)
                ticket_purchase.event = event
                ticket_purchase.user = request.user
                ticket_purchase.save()

                return redirect('user_dashboard')

        context = {
            'event': event,
            'form': form,
        }

        return render(request, 'eventm/buy_tickets.html', context)

    return redirect('user_dashboard')
