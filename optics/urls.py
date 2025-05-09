"""optics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def root_view(request):
    if request.user.is_authenticated:
        return redirect("campaigns")
    return redirect("account_login")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_view, name="root"),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.core.urls")),  # Add this line
]
