from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from numpy import size
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import uuid,random
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.contrib.auth import authenticate,login,logout
# Create your views here.

otp=""
auth_token=""


def home_page(request):

    return render(request,"login/home.html")


def login_here(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        try:
            user_obj=User.objects.get(username=username)
            if user_obj:
                print("exists")
                profile_obj=profile.objects.get(user=user_obj)
                if profile_obj.is_verified:
                    user=authenticate(request,username=username,password=password)
                    if user:
                        login(request,user)
                        print("done")
                    else:
                        print("nt login")
                else:
                    print("NOT VERIFIED")
        except:
            messages.success(request,"INVALID CREDITALS")
            return redirect('/login')
        return redirect('/')
        
    
    return render(request,"login/login.html")

def register_here(request):
    global auth_token
    if request.method=="POST":
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password"]
        
        user_obj=User.objects.create(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token=str(uuid.uuid4())  #storing ;random token
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_email(email,auth_token)
        return redirect('/verification')
        
    return render(request,"login/register.html")

def verification(request):
    #print(otp)
    check=otp[2:]
    #check=int(otp[2:])
    #print(auth_token)
    if request.method=="POST":
        enter_otp=request.POST["otp"]
        #enter_otp=int(enter_otp)
        #print(enter_otp)
        #print(type(check))
        print(type(enter_otp))
        if check==enter_otp:
            print('goodddd goinng')
            user_obj=profile.objects.get(auth_token=auth_token)
            if user_obj:
                user_obj.is_verified=True
                user_obj.save()
                return redirect('/success')
            else:
                print("error")

    return render(request,"login/verification.html")
def success_here(request):
    return render(request,"login/success.html")

def send_email(email,auth_token):
    global otp
    initial="A-"     #authentication OTP initial
    for i in range(5):
        if i==0:
            otp=initial 
        geting_ready= str(random.randint(1,9))  
        otp=otp+geting_ready     #fianl OTP in making
    print(otp)     #OTP
    


    subject = "VERIFICATION PROCESS"
    message="YOUR VERIFICATION PASSCODE is "+ otp
    print(message)
    email_from = settings.EMAIL_HOST_USER
    email_from_pass = settings.EMAIL_HOST_PASSWORD
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(email_from, email_from_pass)
    
    # sending the mail
    s.sendmail(email_from, email,message)
    
    # terminating the session
    s.quit()
    
    
def forgotpass(request):
    return render(request,'login/forgot.html')
    
 




