from django.shortcuts import render
from django.contrib import messages,auth
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from .util import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def check_role_customer(user):
    if user.role == 2:
        return True
    else:
      raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in ")
        return redirect('custDashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # CREATING THE USER USING FORM METHOD 
            password = form.cleaned_data['password']
            user = form.save(commit = False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            
            mail_sub = "Please activate your account"
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_sub, email_template)
            messages.success(request, "Your accounts has been registered sucessfully!")
            return redirect('registerUser')        
    else:
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/registerUser.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
        
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated.")
        return redirect('MyAccount')
    else:
        messages.error(request, "Invalid activation link")
        return redirect('MyAccount') 

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

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email__exact = email)
            
            mail_sub = "Reset your password"
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_sub, email_template)
            
            messages.success(request, "Password reset link has been send to your email address.")
            return redirect('login')
        else:
            messages.success(request, "Account does not exist.")
            return redirect('forgot_password')
    
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk = uid)
        
    except(TypeError, ValueError, OverflowError,User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        
        messages.info(request, "Please reset you password")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('MyAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login')
        else:
            messages.error(request, "Password do not match")
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
 
    