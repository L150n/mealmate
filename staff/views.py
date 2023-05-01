
from django.shortcuts import render,redirect
from accounts.models import *
from django.contrib import messages
from django.http import JsonResponse

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
        messages.success(
                    request, f'Menu item Added.')
        return redirect('/menushow/')
         
    else:
        menu_items = MenuItem.objects.all()
        return redirect('/menushow/')
def edit_menu(request,menuid):
    item = MenuItem.objects.get(menuid=menuid)
    if request.method == 'POST':
        item.item_name = request.POST.get('item_name')
        item.description = request.POST.get('description')
        item.quantity = request.POST.get('quantity')
        item.price = request.POST.get('price')
        if 'menu_image' in request.FILES:
            item.images = request.FILES['menu_image']
        item.save()
        menu_items = MenuItem.objects.all()
        messages.success(
                    request, f'Menu item info edited Successfully .')
        return redirect('/menushow/')
    return redirect('/menushow/')

def delete_menu(request,menuid):
    item = MenuItem.objects.get(menuid=menuid)
    item.delete()
    menu_items = MenuItem.objects.all()
    messages.success(
                    request, f'Menu item Deleted .')
    return redirect('/menushow/')

