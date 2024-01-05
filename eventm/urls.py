from django.urls import path
from .views import  approved_events, rejected_events, approve_event, reject_event, buy_tickets
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("contact", views.contact, name="contact"),
    path("logina_view", views.logina_view, name="logina_view"),
    path("dash_analytics", views.dash_analytics, name="dash_analytics"),
    path("logouta_view", views.logouta_view, name="logouta_view"),
    path("loginu_view", views.loginu_view, name="loginu_view"),
    path("signup_view", views.signup_view, name="signup_view"),
    path("dash_contact", views.dash_contact, name="dash_contact"),
    path("user_dashboard", views.user_dashboard, name="user_dashboard"),
    path('all_events', views.all_events, name='all_events'),
    path('approved_events/', approved_events, name='approved_events'),
    path('rejected_events/', rejected_events, name='rejected_events'),
    path('approve_event/<int:event_id>/', approve_event, name='approve_event'),
    path('reject_event/<int:event_id>/', reject_event, name='reject_event'),
    path('buy-tickets/<int:event_id>/', buy_tickets, name='buy_tickets'),

]
