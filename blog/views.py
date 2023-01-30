from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from .models import Blog
from .models import contact
from .models import Profile, BlogComment
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .helper import send_forgot_password
import uuid


def login(request):
    return render(request,'blog/firstpage.html')

def signuppage(request):
    return render(request,'blog/signup.html')

def handlesignup(request):
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        college=request.POST['college']
        degree=request.POST['degree']
        gender=request.POST['gender']
        dob=request.POST['dob']
        insta_handle=request.POST['insta_handle']
        fb_handle=request.POST['fb_handle']
        twitter_handle=request.POST['twitter_handle']
        phone=request.POST['phone']
        
        # Checks
        if len(username)>15:
            messages.error(request,"Your Username Cannot Be Greater then 15 Characters",extra_tags='hello')
            return redirect('/')

        if not username.isalnum():
            messages.error(request,"Your Username Should Contain only Alphabets and Numbers.",extra_tags='hello')
            return redirect('/')
        
        if pass1!=pass2:
            messages.error(request,"Both of your Passwords should be same",extra_tags='hello')
            return redirect('/')

        if len(phone)!=10:
            messages.error(request,"Your Phone Must have 10 Numbers",extra_tags='hello')
            return redirect('/')

        all_objects=User.objects.all()
        for i in all_objects:
            if i.username==username:
                messages.error(request,"Username already taken.Try Again",extra_tags='hello')
                return redirect('/')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        print(dob)
        myprofile=Profile(profile_user=myuser,degree=degree,college=college,gender=gender,dob=dob,fname=fname,lname=lname,twitter_handle=twitter_handle,insta_handle=insta_handle,fb_handle=fb_handle,email=email,phone=phone)
        myprofile.save()
        messages.success(request,"Your account is Successfully Created.",extra_tags='hello')
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
            messages.error(request,"Wrong Username or Password. Please Try again.",extra_tags='hello')
            return redirect('/')

    return HttpResponse(request,"404 - Page not Found")


def handlelogout(request):
    logout(request)
    messages.success(request,"Logged Out Successfully",extra_tags='hello')
    return redirect('/')


def viewblog(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    comments=BlogComment.objects.filter(post=post).order_by("-timestamp")
    param = {"post":post,"comments":comments}
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

@login_required(login_url='/')
def addblog(request):
    return render(request,'blog/addblog.html')

@login_required(login_url='/')
def postblog(request):
    company_name=request.POST['company_name']
    job_profile=request.POST['job_profile']
    work_ex=request.POST['work_ex']
    experience=request.POST['experience']
    offer_type=request.POST['offer_type']
    curr_user=request.user
    a=Blog(company_name=company_name,job_profile=job_profile,work_ex=work_ex,experience=experience,author=curr_user.username,offer_type=offer_type)
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

@login_required(login_url='/')
def saveblog(request,id):
    post=Blog.objects.filter(id=id).first()
    post.favourites.add(request.user)
    return redirect('/saved')
    
@login_required(login_url='/')
def rendersaved(request):
    all_objects=Blog.objects.filter(favourites=request.user)
    param={'all_objects':all_objects}
    return render(request,'blog/savedblogs.html',param)

@login_required(login_url='/')
def remsave(request,id):
    post=Blog.objects.filter(id=id).first()
    post.favourites.remove(request.user)
    return redirect('/saved')

@login_required(login_url='/')
def editblog(request,slug):
    post = Blog.objects.filter(slug=slug).first()
    curr_user=request.user
    if post.author == curr_user.username:
        param = {"post":post}
        return render(request,'blog/editblog.html',param)
    else:
        return redirect('/home')

@login_required(login_url='/')
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

@login_required(login_url='/')
def profile(request,username):
    i=User.objects.filter(username=username).first()
    #print(i)
    j=Profile.objects.filter(profile_user=i).first()
    param={"i":i, "j":j}
    return render(request,'blog/viewprofile.html',param)

@login_required(login_url='/')
def deleteblog(request,slug):
    i=Blog.objects.filter(slug=slug).first()
    i.delete()
    return redirect('/myblogs')

def cpass(request,username):
    print(username)
    return render(request,'blog/changepass.html')


def savepass(request):
    i=request.user
    oldpass=request.POST['oldpass']
    newpass1=request.POST['newpass1']
    newpass1=request.POST['newpass2']
    i.set_password(newpass1)
    i.save()
    return redirect('/')

@login_required(login_url='/')
def editprof(request,user):
    i=User.objects.filter(username=user).first()
    j=Profile.objects.filter(profile_user=i).first()
    params={'j':j}
    return render(request,'blog/editprof.html',params)

@login_required(login_url='/')
def saveprofile(request):
    if request.method=="POST":
        email=request.POST['email']
        college=request.POST['college']
        degree=request.POST['degree']
        insta_handle=request.POST['insta_handle']
        fb_handle=request.POST['fb_handle']
        twitter_handle=request.POST['twitter_handle']
        phone=request.POST['phone']
        i=request.user
        Profile.objects.filter(profile_user=i).update(email=email,college=college,degree=degree,insta_handle=insta_handle,fb_handle=fb_handle,phone=phone,twitter_handle=twitter_handle)
        return redirect(f'/profile/{i}')

@login_required(login_url='/')
def postcomment(request):
    if request.method=="POST":
        comment=request.POST.get("comment")
        user=request.user
        print(user)
        postID=request.POST.get("postID")
        post=Blog.objects.filter(id=postID).first()
        post_comment=BlogComment(comment=comment,user=user,post=post)
        post_comment.save()

        return redirect(f'view/{post.slug}')


def fprender(request):
    # if request.method=='POST':
        return render(request,'blog/forgotpass.html')

def forgotpass(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if not User.objects.filter(username=username).first():
            messages.warning(request,'Enter a valid username')
            return redirect('/forgotpass')

        user_obj=User.objects.get(username=username)
        token = str(uuid.uuid4())
        prof_obj = Profile.objects.get(profile_user = user_obj)
        prof_obj.forget_pass_token=token
        prof_obj.save()
        send_forgot_password(user_obj,token)
        messages.success(request,'An E-mail is sent to you.')
        return redirect('/forgotpass')


def changepass(request,token):
    prof_obj=Profile.objects.filter(forget_pass_token = token).first()
    param={"prof_obj":prof_obj.profile_user.username}
    return render(request,'blog/cpassemail.html',param)


def cpassemail(request,token):
    if request.method=='POST':
        newpass1=request.POST.get('pass1')
        newpass2=request.POST.get('pass2')
        user_username=request.POST.get('prof_obj')

        if user_username is None:
            messages.success(request,"No User Found")
            return redirect(f'/changepass{token}')

        if newpass1 != newpass2:
            messages.success(request,"Enter Password Correctly")
            return redirect(f'/changepass{token}')

        user_obj=User.objects.get(username=user_username) 
        user_obj.set_password=newpass1
        user_obj.save()
        return redirect('/login') 