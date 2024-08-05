from django.http import HttpResponse
from django.shortcuts import render

from service.models import login

from django.core.mail import send_mail
from django.db import connection
import random

tokennumber=0
# def index(request):
#     m=""
#     if 'ss' in request.session:
#         if request.method=="POST":
#             H=request.POST.get('i1')
#             D=request.POST.get('i2')
#             request.session['a']=D
#             return render(request,"hospital__appoint.html") 
        
#     else:
#         m="your session has expired please login again"
#         return render(request,"home.html",{'m':m})
    
def index(request):
    return render(request,"inde.html")

# def forget(request):
#     if request.method=="POST":
#             email=request.POST.get('email')

def loginn(request):
    
    return render(request,"login.html")
    
       
def login1(request):
        m=""
        if request.method=="POST":
            email=request.POST.get('email')
            password=request.POST.get('password')
            count=0
            a=login.objects.raw("select * from service_login")
            for i in a:
                if i.email==email:
                    count=1
                    p=i.password
                    
            if count==0:
               m="no such email id found"  
               return render(request,"login.html",{'m':m}) 
                
            else:
                if password==p:
                    m="login success"
                    request.session['ss']=email
                    return render(request,"inde.html",{'m':m})
                else:
                    m="incorrect password"
                    return render(request,"login.html",{'m':m})

def registerform(request):
    return render(request,"register.html")
                    
def register(request):
        m=""
        if request.method=="POST":
            email=request.POST.get('email')
            name=request.POST.get('name')
            password=request.POST.get('password')
            count=0
            a=login.objects.raw("select * from service_login")
            for i in a:
                if i.email==email:
                    count=count+1
                    
                    
            if count!=0:
               m="email id already exist"  
               return render(request,"register.html",{'m':m}) 
                
            else:
                OTP = random.randint(11111,99999)
                send_mail(
                'OTP',
                "your login otp is " +str(OTP),
                'useriiitk01@gmail.com',
                [email],
                )
                request.session['otp']= str(OTP)
                request.session['email']= email
                request.session['name']= name
                request.session['password']= password
                
                return render(request,"otppage.html",{'m':m})
            
def otppage(request):
    m=""
    print("hi")
    if 'otp' in request.session:
        if request.method=="POST":
            otp=request.POST.get('otp')
            
            OTP=request.session['otp']
            print(OTP)
            print(otp)
            if OTP==otp:
                email=request.session['email']
                name=request.session['name']
                password=request.session['password']
                log=login(name=name, email=email, password=password)
                log.save()
                m="registration success"
                return render(request,"login.html",{'m':m})
            else:
                m="incorrect otp"
                return render(request,"otppage.html",{'m':m})
            
def order1(request):
    if 'ss' in request.session:
        if request.method=="POST":
            name=request.POST.get('ordername')
            request.session['ordername']=name
        return render(request,"order.html")
    else:
        
        return render(request,"login.html")
    
def orderq(request):
    if 'ss' in request.session:
        if request.method=="POST":
            quantity=request.POST.get('quantity')
            ins=request.POST.get('ins')
            name=request.POST.get('ordername')
            email=request.session['ss']
            print(name)
            print(email)
            print(ins)
            print(quantity)
            print(email)
            global tokennumber
            tokennumber=tokennumber+1
            
            send_mail(
                'order details',
                "order name :" +name+"\n"+"instructions :"+ins+"\n"+"tokennumber: "+str(tokennumber)+"\n"+"quantity: "+quantity+"\n"+"order received" ,
                'useriiitk01@gmail.com',
                [email],
            )
            print("hi")
            print()
            
        return render(request,"inde.html")
    else:
        
        return render(request,"login.html")
    
def ordere(request):
    
    if 'ss' in request.session:
        if request.method=="POST":
            quantity=request.POST.get('quantity')
            ins=request.POST.get('ins')
            name=request.session['ordername']
            email=request.session['ss']
            global tokennumber
            tokennumber=tokennumber+1
            send_mail(
                'order details',
                "order name :" +name+"\n"+"instructions :"+ins+"\n"+"tokennumber: "+str(tokennumber)+"\n"+"quantity: "+quantity+"\n"+"order received" ,
                'useriiitk01@gmail.com',
                [email],
            )
            print("hi")
            print()
            return render(request,"inde.html")
    else:   
        return render(request,"login.html")
    
              
def logout(request):
    if 'ss' in request.session:
        del request.session['ss']
        return render(request,"inde.html")
    else:
        
        return render(request,"login.html")

def forgetpas(request):
    return render(request,"forgot.html")
    
    
    
def forgetpass(request):
    count=0
    m=""
    print("hi")
    if request.method=="POST":
            email=request.POST.get('email')
            a=login.objects.raw("select * from service_login")
            for i in a:
                if i.email==email:
                    count=count+1
            print(count)
            if count==0:
                  m="no such email exist please register"
                  return render(request,"forgot.html",{'m':m})
            else:
                OTP = random.randint(11111,99999)
                send_mail(
                'OTP',
                "your login otp is " +str(OTP),
                'useriiitk01@gmail.com',
                [email],
                )
                request.session['otp1']= str(OTP)
                request.session['email1']= email
                return render(request,"otpp.html",{'m':m})
            
def enterotp(request):
    m=""
    if request.method=="POST":
        otp=request.POST.get('otp')
        OTP=request.session['otp1']
        email=request.session['email1']
        if otp==OTP:
            request.session['email2']=email
            
            return render(request,"reset.html")
        else:
            m="incorrect otp"
            return render(request,"otpp.html",{'m':m})
        
def final(request):
    m=""
    if request.method=="POST":
        password=request.POST.get('password')
        email=request.session['email2']
        log=connection.cursor()
        log.execute("UPDATE service_login SET password = %s WHERE email= %s",(password, email))
        m="password updated successfully"
        return render(request,"login.html",{'m':m})
        
        
        
        
            
        
            

                
                 
           
            
    
    
                                
        
                  
                
                
                
                
                     
                    