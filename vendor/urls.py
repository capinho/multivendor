"""vendor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('become-vendor/', views.become_vendor,name='become_vendor'),
    path('vendor-admin/', views.vendor_admin,name='vendor_admin'),
    path('add-product/', views.add_procduct,name='add_product'),
    path('edit-vendor/', views.edit_vendor,name='edit_vendor'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),


]
