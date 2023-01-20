from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from .models import Blog

def login(request):
    return render(request,'blog/login.html')

def handlesignup(request):
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        
        # Checks
        if len(username)>15:
            messages.error(request,"Your Username Cannot Be Greater then 15 Characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(request,"Your Username Should Contain only Alphabets and Numbers.")
            return redirect('/')
        
        if pass1!=pass2:
            messages.error(request,"Both of your Passwords should be same")
            return redirect('/')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your account is Successfully Created.")
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')


def home(request):
    print("home")
    all_objects=Blog.objects.all()
    param={"all_objects":all_objects}

    return render(request,'blog/home.html',param)

def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']

        user=authenticate(request,username=loginusername,password=loginpass)

        if user is not None:
            auth_login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/home')
        else:
            messages.error(request,"Wrong Username or Password. Please Try again.")
            return redirect('/')

    return HttpResponse(request,"404 - Page not Found")


def handlelogout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return redirect('/')


def viewblog(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    param = {"post":post}
    return render(request,'blog/viewblog.html',param)


def search(request):
    query=request.GET['query']
    print(query)
    all_objects=Blog.objects.get(company_name__icontains=query)
    params={'all_objects':all_objects}
    return render (request,'/blog/search.html',params)


def aboutus(request):
    print("here")
    return render(request,'/blog/aboutus.html')