from django.shortcuts import render, redirect
from .forms import VendorForm
from .models import Vendor
from accounts.models import User, UserProfile
from accounts.forms import UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Checking the access for the user
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
      raise PermissionDenied

@login_required(login_url = 'login')
def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in ")
        return redirect('MyAccount')
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            
            # CREATED User USING THE CLASS METHOD
            password = form.cleaned_data['password']
            user = form.save(commit = False)
            user.set_password(password)
            user.role = User.RESTAURANT
            print(user.role)
            user.save()
        
            vendor = v_form.save(commit=False)
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            messages.success(request, "Your accounts has been registered sucessfully! Please wait for the approval.")
            return redirect('login') 
        else:
            print(form.errors)
            
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form' : form,
        'v_form' : v_form
    }
    return render(request, 'vendor/registerVendor.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def vendorDashboard(request):
    return render(request, 'vendor/vendorDashboard.html')