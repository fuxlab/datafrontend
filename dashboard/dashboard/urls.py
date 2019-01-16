"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from notes import endpoints as notes_endpoints
from projects import endpoints as projects_endpoints
from datasets import endpoints as datasets_endpoints

urlpatterns = [
    url(r'^api/', include(notes_endpoints)),
    url(r'^api/', include(projects_endpoints)),
    url(r'^api/', include(datasets_endpoints)),
    url(r'^', TemplateView.as_view(template_name="index.html")),
]