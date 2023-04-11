
from django.shortcuts import render,redirect
from accounts.models import *

def indexstaff(request):
    return render(request,'index_staff.html')
def menushow(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_staff.html', {'menu_items': menu_items})
def addmenu(request):
    if request.method == 'POST':
        item_name = request.POST.get('item-name')
        item_description = request.POST.get('item-description')
        item_quantity = request.POST.get('item-quantity')
        item_price = request.POST.get('item-price')
        item_image = request.FILES.get('item-image')
        MenuItem.objects.create(item_name=item_name, description=item_description, quantity=item_quantity, price=item_price, images=item_image)
        menu_items = MenuItem.objects.all()
        return render(request, 'menu_staff.html', {'menu_items': menu_items})
        
    
    else:
        menu_items = MenuItem.objects.all()
        return render(request, 'menu_staff.html', {'menu_items': menu_items})
        