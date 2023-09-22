from django.shortcuts import render, redirect
from .forms import VendorForm
from .models import Vendor
from accounts.models import User, UserProfile
from accounts.forms import UserForm
from django.contrib import messages


# Create your views here.
def registerVendor(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            # CREATED USER USING THE CLASS METHOD
            first_name  = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email  = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = User.objects.create(username= username, first_name = first_name, last_name = last_name, email = email, password = password)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user 
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your accounts has been registered sucessfully! Please wait for the approval.")
            return redirect('registerVendor') 
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