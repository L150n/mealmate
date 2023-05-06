from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    
    path('indexstaff/', views.indexstaff, name='indexstaff'),
    path('menushow/', views.menushow, name='menushow'),
    path('addmenu/', views.addmenu, name='addmenu'),
    path('order_staff/', views.order_staff, name='order_staff'),
    path('delete_menu/<int:menuid>/', views.delete_menu, name='delete_menu'),
    path('edit_menu/<int:menuid>/', views.edit_menu, name='edit_menu'),
    path('check_face/', views.check_face, name='check_face'),
    path('add_to_cart_staff/<int:item_id>/<int:student_id>/', views.add_to_cart_staff, name='add_to_cart_staff'),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)