from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static



app_name="staff"

urlpatterns = [
    
    path('indexstaff/', views.indexstaff, name='indexstaff'),
    path('menushow/', views.menushow, name='menushow'),
    path('addmenu/', views.addmenu, name='addmenu'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)