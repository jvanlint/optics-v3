from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def reference_tables(request):
    return render(request, "reference_tables.html")

def threat_database(request):
    return render(request, "threat_database.html")

def faq(request):
    return render(request, "faq.html")

def profile(request):
    return render(request, "profile.html")

def profile_edit(request):
    return render(request, "profile_edit.html")

def change_password(request):
    return render(request, "change_password.html")

def system_health_dashboard(request):
    return render(request, "system_health_dashboard.html")

def campaigns(request):
    return render(request, "index.html")