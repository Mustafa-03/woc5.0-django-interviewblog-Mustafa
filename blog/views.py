from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from .models import Blog
from .models import contact
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

def login(request):
    return render(request,'blog/firstpage.html')

def handlesignup(request):
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        profile_pic=request.FILES['profile']
        
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
        # fss = FileSystemStorage()
        # file = fss.save(profile.name, profile)
        # file_url = fss.url(file)
        # myprofile=Profile.objects.create(profile_user=myuser,profile_pic=file_url,Degree="123",College="456")
        # myprofile.save()
        messages.success(request,"Your account is Successfully Created.")
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')


def home(request):
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
    company_objects=Blog.objects.filter(company_name__icontains=query)
    author_objects=Blog.objects.filter(author__icontains=query)
    job_profile_objects=Blog.objects.filter(job_profile__icontains=query)
    params={'company_objects':company_objects,'author_objects':author_objects,'job_profile_objects':job_profile_objects}
    return render (request,'blog/search.html',params)


def abts(request):
    return render(request,'blog/abts.html')

def contactus(request):
    return render(request,'blog/contactus.html')


def addblog(request):
    return render(request,'blog/addblog.html')

def postblog(request):
    company_name=request.POST['company_name']
    job_profile=request.POST['job_profile']
    work_ex=request.POST['work_ex']
    experience=request.POST['experience']
    if company_name=="" or job_profile=="" or work_ex=="" or experience=="":
        messages.error("Invalid Post.Please Try Again Later")
    curr_user=request.user
    a=Blog(company_name=company_name,job_profile=job_profile,work_ex=work_ex,experience=experience,author=curr_user.username)
    a.save()

    return redirect('/home')

@login_required(login_url='/')
def myblogs(request):
    curr_user=request.user
    author_objects=Blog.objects.filter(author__icontains=curr_user.username)
    params={'author_objects':author_objects}
    return render (request,'blog/myblogs.html',params)


def submitquery(request):
    name=request.POST['contact_name']
    username=request.POST['contact_username']
    query=request.POST['contact_query']
    a=contact(name=name,username=username,query=query)
    a.save()

    return redirect('/')

def saveblog(request,id):
    post=Blog.objects.filter(id=id).first()
    post.favourites.add(request.user)
    
    return redirect('/saved')
    

def rendersaved(request):
    all_objects=Blog.objects.filter(favourites=request.user)
    param={'all_objects':all_objects}
    return render(request,'blog/savedblogs.html',param)

def remsave(request,id):
    post=Blog.objects.filter(id=id).first()
    post.favourites.remove(request.user)
    return redirect('/saved')


def editblog(request,slug):
    post = Blog.objects.filter(slug=slug).first()
    param = {"post":post}
    return render(request,'blog/editblog.html',param)

def edit(request):
    company_name=request.POST['company_name']
    job_profile=request.POST['job_profile']
    work_ex=request.POST['work_ex']
    experience=request.POST['experience']
    id=request.POST['id']
    if company_name=="" or job_profile=="" or work_ex=="" or experience=="":
        messages.error("Invalid Post.Please Try Again Later")
        return redirect('/myblogs')
    curr_user=request.user
    Blog.objects.filter(id=id).update(job_profile=job_profile,company_name=company_name,work_ex=work_ex,experience=experience)
    return redirect('/myblogs')

def profile(request,username):
    i=User.objects.filter(username=username).first()
    param={"i":i}
    return render(request,'blog/viewprofile.html',param)

def deleteblog(request,slug):
    i=Blog.objects.filter(slug=slug).first()
    print(i)
    i.delete()
    return redirect('/myblogs')