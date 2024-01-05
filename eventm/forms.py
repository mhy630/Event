from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ContactFormEntry, Event, Ticket
class LoginaForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class LoginuForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormEntry
        fields = ['name', 'email', 'message']
class EventForm(forms.ModelForm):
    EVENT_TYPE_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('concert', 'Concert'),
        ('wedding', 'Wedding')
        # Add more choices as needed
    ]

    event_type = forms.ChoiceField(choices=EVENT_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'event_type']
        
class TicketPurchaseForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['tickets_purchased']
        
        