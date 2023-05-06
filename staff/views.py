
from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import *
from django.contrib import messages
from django.http import JsonResponse,Http404
from django.utils.html import format_html
import face_recognition
import base64
import cv2
from PIL import Image
import io 
import numpy as np
from django.http import HttpResponse

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
        messages.success(
                    request, f'Menu item Added.')
        return redirect('/menushow/')
         
    else:
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
        messages.success(request, f'Menu item info edited Successfully .')
        return redirect('/menushow/')
    return redirect('/menushow/')

def delete_menu(request,menuid):
    item = MenuItem.objects.get(menuid=menuid)
    item.delete()
    menu_items = MenuItem.objects.all()
    messages.success(
                    request, f'Menu item Deleted .')
    return redirect('/menushow/')

def order_staff(request):
    return render(request,'order_staff.html')

def check_face(request):
    if request.method == 'POST':
        captured_image_data = request.POST.get('image_data')
        captured_image_binary = base64.b64decode(captured_image_data.split(',')[1])

        # Load the captured image
        captured_image = face_recognition.load_image_file(io.BytesIO(captured_image_binary))
        captured_image_encodings = face_recognition.face_encodings(captured_image)

        # Check if any face is detected in the captured image
        if len(captured_image_encodings) == 0:
            messages.error(request, 'No face found. Scan again!')
            return render(request, 'order_staff.html')

        captured_image_encoding = captured_image_encodings[0]
        # Load all the student images from the database
        student_images = StudentImage.objects.all()

        # Compare the captured image with each student image
        for student_image in student_images:
            # Load the student image from the database
            student_image_binary = student_image.image
            student_image_stream = io.BytesIO(student_image_binary)
            student_image_array = face_recognition.load_image_file(student_image_stream)
            student_image_encoding = face_recognition.face_encodings(student_image_array)[0]

            # Compare the encodings
            matches = face_recognition.compare_faces([student_image_encoding], captured_image_encoding)
            if matches[0]:
                # If a match is found, return the corresponding student ID
                student = get_object_or_404(Student, pk=student_image.studentid_id)
                menu_items = MenuItem.objects.all()
                messages.success(request,format_html('Student <strong>{} {}</strong> with Admission No : <strong>{}</strong> found successfully.'.format(student.first_name, student.last_name, student.studentid)))
                return render(request, 'order_staff.html', {'student': student , 'menu_items': menu_items})
        messages.error(request,'Student not found. Scan again!')
        return render(request, 'order_staff.html')

    return render(request, 'order_staff.html')


def add_to_cart_staff(request, item_id, student_id):
    menu_itemsall = MenuItem.objects.all()
    try:
        menu_item = MenuItem.objects.get(menuid=item_id)
    except MenuItem.DoesNotExist:
        raise Http404('Menu item not found')

    # Get the student object
    student = get_object_or_404(Student, pk=student_id)

    # Check if the student already has a cart
    cart, created = Cart.objects.get_or_create(studentid=student)

    # Check if the cart already contains the maximum number of items
    if cart.item1 and cart.item2 and cart.item3 and cart.item4 and cart.item5:
        messages.error(request, f"Maximum number of items already in cart for student {student.first_name}")

    # Add the selected item to the cart
    if not cart.item1:
        cart.item1 = menu_item
        menu_item.quantity -= 1
    elif not cart.item2:
        cart.item2 = menu_item
        menu_item.quantity -= 1
    elif not cart.item3:
        cart.item3 = menu_item
        menu_item.quantity -= 1
    elif not cart.item4:
        cart.item4 = menu_item
        menu_item.quantity -= 1
    elif not cart.item5:
        cart.item5 = menu_item
        menu_item.quantity -= 1

    messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")
    cart.save()
    menu_item.save()
    return render(request, 'order_staff.html', {'student': student , 'menu_items': menu_itemsall})
