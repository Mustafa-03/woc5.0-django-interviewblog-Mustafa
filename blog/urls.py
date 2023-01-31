from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.login,name="Index"),
    path('signuppage',views.signuppage,name="Sign Up Page"),
    path('signup',views.handlesignup,name="Sign Up"),
    path('home',views.home,name="Home"),
    path('login',views.handlelogin,name="Log in"),
    path('logout',views.handlelogout,name="Log Out"),
    path('view/profile/<str:username>',views.profile,name="profile"),
    path('view/<str:slug>',views.viewblog,name="View Blog"),
    path('search',views.search,name='search'),
    path('abts',views.abts,name="abts"),
    path('contactus',views.contactus,name="contactus"),
    path('addblog',views.addblog,name="addblog"),
    path('postblog',views.postblog,name="postblog"),
    path('myblogs',views.myblogs,name="myblogs"),
    path('submitquery',views.submitquery,name="submitquery"),
    path('save/<str:id>',views.saveblog,name="saveblog"),
    path('saved',views.rendersaved,name="rendersaved"),
    path('remsave/<str:id>',views.remsave,name="remsave"),
    path('editblog/<str:slug>',views.editblog,name="editblog"),
    path('edit',views.edit,name="edit"),
    path('profile/<str:username>',views.profile,name="profile"),
    path('delblog/<str:slug>',views.deleteblog,name="deleteblog"),
    path('cpass/<str:username>',views.cpass,name="Change Password"),
    path('savepass',views.savepass,name="Save Password"),
    path('profile/editprof/<str:user>',views.editprof,name="Edit Profile"),
    path('saveprofile',views.saveprofile,name="Save Profile"),
    path('postcomment',views.postcomment,name="postcomment"),
    path('forgotpass',views.fprender,name="Forgot Password"),
    path('fpfunc',views.forgotpass,name="Forgot Password Function"),
    path('changepass/<str:token>',views.changepass,name="Change Password with email"),
    path('savechangepass',views.cpassemail,name="Save The Changed Password")
]