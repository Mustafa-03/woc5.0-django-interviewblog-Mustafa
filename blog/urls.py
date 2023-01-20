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
    path('<str:slug>',views.viewblog,name="View Blog"),
    path('aboutus',views.aboutus,name="Aboutus")

]