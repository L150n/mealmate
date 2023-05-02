from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    
    path('indexstaff/', views.indexstaff, name='indexstaff'),
    path('menushow/', views.menushow, name='menushow'),
    path('addmenu/', views.addmenu, name='addmenu'),
    path('delete_menu/<int:menuid>/', views.delete_menu, name='delete_menu'),
    path('edit_menu/<int:menuid>/', views.edit_menu, name='edit_menu'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)