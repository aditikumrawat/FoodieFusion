from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # CREATING THE USER USING FORM METHOD 
            # password = form.cleaned_data['password']
            # user = form.save(commit = False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # CREATED USER USING THE CLASS METHOD
            first_name  = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email  = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            user = User.objects.create(username= username, first_name = first_name, last_name = last_name, email = email, password = password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your accounts has been registered sucessfully!")
            return redirect('registerUser')        
    else:
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/registerUser.html', context)