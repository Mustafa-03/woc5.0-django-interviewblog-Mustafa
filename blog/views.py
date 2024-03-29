from django.http import HttpResponse
from django.http import HttpResponseRedirect
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
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import datetime


def login(request):
    return render(request,'blog/firstpage.html')

def signuppage(request):
    return render(request,'blog/signup.html')

def handlesignup(request):
    if request.method=="POST":
        username=request.POST['username']
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
        currwork=request.POST['curwork']
        image=request.FILES['image']
        
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
        myprofile=Profile(profile_user=myuser,degree=degree,college=college,gender=gender,dob=dob,fname=fname,lname=lname,twitter_handle=twitter_handle,insta_handle=insta_handle,fb_handle=fb_handle,email=email,phone=phone,profile_pic=image,currwork=currwork)
        myprofile.save()
        messages.success(request,"Your account is Successfully Created.",extra_tags='hello')
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')

def home(request):
    all_objects=Blog.objects.all().order_by('-updated_at')
    paginator = Paginator(all_objects, 3)
    page = request.GET.get('page')
    bg=paginator.get_page(page)
    param={"bg":bg}

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
    company_objects=Blog.objects.filter(company_name__icontains=query).order_by('-updated_at') | Blog.objects.filter(author__icontains=query).order_by('-updated_at') | Blog.objects.filter(job_profile__icontains=query).order_by('-updated_at')
    paginator = Paginator(company_objects, 3)
    page = request.GET.get('page')
    bg=paginator.get_page(page)
    params={'company_objects':company_objects,'bg':bg}
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
    paginator = Paginator(author_objects, 3)
    page = request.GET.get('page')
    bg=paginator.get_page(page)
    params={'bg':bg}
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
    # return HttpResponseRedirect(request.path_info)
    
@login_required(login_url='/')
def rendersaved(request):
    all_objects=Blog.objects.filter(favourites=request.user).order_by('-updated_at')
    paginator = Paginator(all_objects, 3)
    page = request.GET.get('page')
    bg=paginator.get_page(page)
    param={'bg':bg}
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
    current_datetime = datetime.datetime.now()
    curr_user=request.user
    Blog.objects.filter(id=id).update(job_profile=job_profile,company_name=company_name,work_ex=work_ex,experience=experience,updated_at=current_datetime)
    return redirect('/myblogs')

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
        currwork=request.POST['curwork']
        image=request.FILES['image']
        i=request.user
        prof=Profile.objects.get(profile_user=i)
        prof.email=email
        i.email=email
        prof.college=college
        prof.degree=degree
        prof.insta_handle=insta_handle
        prof.fb_handle=fb_handle
        prof.phone=phone
        prof.twitter_handle=twitter_handle
        prof.currwork=currwork
        prof.profile_pic=image
        prof.save()
        #prof=Profile.objects.filter(profile_user=i).update(profile_pic=image)
        return redirect(f'/profile/{i}')

def postcomment(request):
    if request.method=="POST":
        curr_user=request.user
        comment=request.POST.get("comment")
        postID=request.POST.get("postID")
        post=Blog.objects.filter(id=postID).first()
        if curr_user.is_authenticated:
            post_comment=BlogComment(comment=comment,user=curr_user,post=post)
            post_comment.save()
            messages.error(request,"Comment Posted Successfully",extra_tags='hello')
            return redirect(f'view/{post.slug}')
        else:
            messages.error(request,"Please Log in to Comment",extra_tags='hello')
            return redirect(f'view/{post.slug}')

def fprender(request):
    return render(request,'blog/forgotpass.html')

def forgotpass(request):
    if request.method=='POST':
        username=request.POST.get('username')
        if not User.objects.filter(username=username).first():
            messages.warning(request,'Enter a valid username',extra_tags='hello')
            return redirect('/forgotpass')

        user_obj=User.objects.get(username=username)
        token = str(uuid.uuid4())
        prof_obj = Profile.objects.get(profile_user = user_obj)
        prof_obj.forget_pass_token=token
        prof_obj.save()
        send_forgot_password(prof_obj.email,token)
        messages.success(request,'An E-mail is sent to you.',extra_tags='hello')
        return redirect('/forgotpass')

def changepass(request,token):
    prof_obj=Profile.objects.filter(forget_pass_token = token).first()
    param={"prof_obj":prof_obj.profile_user.username}
    return render(request,'blog/cpassemail.html',param)

def cpassemail(request):
    if request.method=='POST':
        newpass1=request.POST['pass1']
        newpass2=request.POST['pass2']
        user_username=request.POST['prof_obj']

        if user_username is None:
            messages.success(request,"No User Found",extra_tags='hello')
            return redirect(f'/forgotpass')

        if newpass1 != newpass2:
            messages.success(request,"Enter Password Correctly",extra_tags='hello')
            return redirect(f'/forgotpass')
        user_obj=User.objects.filter(username=user_username).first()
        user_obj.set_password(newpass1)
        user_obj.save()
        messages.success(request,"Password Changed Successfully",extra_tags='hello')
        return redirect('/') 

def delcomm(request):
    if request.method=='POST':
        comid=request.POST['comid']
        postid=request.POST['compost']
        post=Blog.objects.filter(id=postid).first()
        delpost=BlogComment.objects.filter(sno=comid).first()
        user=request.POST['comuser']
        if user == request.user.username:
            messages.success(request,"Comment deleted successfully",extra_tags='hello')
            delpost.delete()
        else:
            messages.warning(request,"You are not allowed to delete this comment",extra_tags='hello')

    return redirect(f'view/{post.slug}')
