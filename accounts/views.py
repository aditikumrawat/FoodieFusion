from django.shortcuts import render
from django.contrib import messages,auth
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from .util import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
      raise PermissionDenied
  

        

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in ")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # CREATING THE USER USING FORM METHOD 
            password = form.cleaned_data['password']
            user = form.save(commit = False)
            user.set_password(password)
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


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('MyAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Your are now logged in")
            return redirect('MyAccount')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')


@login_required(login_url = 'login')
def MyAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url = 'login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custdashboard.html')

