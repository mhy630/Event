# Event Management System

This Django project implements an Event Management System with facial recognition for admin authentication.

## Features

- User authentication using facial recognition.
- Event creation, registration, and approval/rejection functionalities.
- User dashboard with event details and analytics.
- Contact form for user inquiries.

## Main Functions

- User can create and account and login to his dashboard.
- User can request and event and see its status.
- User can buy tickets for other active events.
- Admin can login to his dashboard with facial rcognition adding extra layer of security.
- Admin can view pending events, approve them or reject them.

## Usage

1. Users can navigate to the index page.
2. Admins can add new events and view contact form entries.
3. Users can log in using facial recognition or regular credentials.
4. Authenticated users can view their dashboard, register for events, and purchase tickets.

## Implementation

1. Create a Django Project:

2. django-admin startproject myproject
   cd myproject

3. Create a Django App:
   python manage.py startapp eventm

4. Create Database Tables:
   python manage.py makemigrations
   python manage.py migrate

5. Setup Views Functions
   Set Up Forms:

6. Integrate Third-Party Libraries:
   Make sure to install the required third-party libraries using:
   
   pip install face_recognition matplotlib

7. Configure URLs:
Edit myproject/urls.py to include URL patterns for your app.

8. Set Up Templates:
   Create HTML templates in the eventm/templates directory. Use these templates to render the views.

9. Configure Django Settings:
   Adjust Django settings in myproject/settings.py. Make sure to include your app in the INSTALLED_APPS section.

10. Run the Development Server:
    python manage.py runserver

## Additional Notes
Ensure that the paths in functions like convert_base64_to_image are adjusted according to your system.
Handle media files and static files configurations in Django settings.
The implementation might involve creating HTML templates for rendering views, which are not provided in the code snippet.
Consider adding user authentication URLs and templates if not already included.




Feel free to explore and modify the code according to your needs.