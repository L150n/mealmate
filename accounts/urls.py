from django.urls import path
from . import views

app_name="accounts"

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('profile/',views.profile,name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_pass/', views.update_pass, name='update_pass'),
    path('index/',views.index,name='index'),
    path('reg/', views.reg, name='reg'),
    path('loginuser/', views.loginuser, name='loginuser'),
] 