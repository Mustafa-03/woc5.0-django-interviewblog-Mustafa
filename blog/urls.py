from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('',views.login,name="Index"),
    path('signup',views.handlesignup,name="Sign Up"),
    path('home',views.home,name="Home"),
    path('login',views.handlelogin,name="Log in"),
    path('logout',views.handlelogout,name="Log Out"),
    path('view/<str:slug>',views.viewblog,name="View Blog"),
    path('search',views.search,name='search'),
    path('abts',views.abts,name="abts"),
    path('contactus',views.contactus,name="contactus"),
    path('addblog',views.addblog,name="addblog"),
    path('postblog',views.postblog,name="postblog"),
    path('myblogs',views.myblogs,name="myblogs"),
    path('submitquery',views.submitquery,name="submitquery"),
    path('saveblog',views.saveblog,name="saveblog")
    
    
]