from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('ewallet/', views.ewallet, name='ewallet'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_pass/', views.update_pass, name='update_pass'),
    path('process_image/', views.process_image, name='process_image'),
    path('index/', views.index, name='index'),
    path('reg/', views.reg, name='reg'),
    path('login_view/', views.login_view, name='login_view'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('menushowstudent/', views.menushowstudent, name='menushowstudent'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

