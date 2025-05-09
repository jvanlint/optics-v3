from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    index,
    reference_tables,
    threat_database,
    faq,
    profile,
    profile_edit,
    change_password,
    system_health_dashboard,
    campaigns,
)

urlpatterns = [
    path('campaigns/', campaigns, name='campaigns'),
    path('reference-tables/', reference_tables, name='reference_tables'),
    path('threat-database/', threat_database, name='threat_database'),
    path('faq/', faq, name='faq'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('change-password/', change_password, name='change_password'),
    path('system-health/', system_health_dashboard, name='system_health_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]