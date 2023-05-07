
from django.shortcuts import render,redirect, get_object_or_404
from accounts.models import *
from django.contrib import messages
from django.http import JsonResponse,Http404
from django.utils.html import format_html
import face_recognition
import base64
from decimal import Decimal
import cv2
from PIL import Image
import io 
import numpy as np
from django.http import HttpResponse
student_id = None 
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
                global student_id 
                student_id = student.studentid 
                menu_items = MenuItem.objects.all()
                messages.success(request,format_html('Student <strong>{} {}</strong> with Admission No : <strong>{}</strong> found successfully.'.format(student.first_name, student.last_name, student.studentid)))
                return render(request, 'order_staff.html', {'student': student , 'menu_items': menu_items})
        messages.error(request,'Student not found. Scan again!')
        return render(request, 'order_staff.html')

    return render(request, 'order_staff.html')


def add_to_cart_staff(request, item_id):
    menu_itemsall = MenuItem.objects.all()
    cartall = Cart.objects.filter(studentid=student_id)
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
        messages.warning(request, f"Maximum number of items already in cart for student {student.first_name}")

    # Add the selected item to the cart
    if not cart.item1:
        cart.item1 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")
    elif not cart.item2:
        cart.item2 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")
    elif not cart.item3:
        cart.item3 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")
    elif not cart.item4:
        cart.item4 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")
    elif not cart.item5:
        cart.item5 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f"{menu_item.item_name} added to cart for student {student.first_name}")

    cart.save()
    menu_item.save()
    return render(request, 'order_staff.html', {'student': student , 'menu_items': menu_itemsall , 'carts':cartall})
def delete_cart_item(request, cart_id, item_number):
    menu_itemsall = MenuItem.objects.all()
    cartall = Cart.objects.filter(studentid=student_id)
    cart = Cart.objects.get(cartid=cart_id)
    student = get_object_or_404(Student, pk=student_id)
    # Get the menu item from the cart based on the item number
    if item_number == 'item1':
        menu_item = cart.item1
        cart.item1 = None
    elif item_number == 'item2':
        menu_item = cart.item2
        cart.item2 = None
    elif item_number == 'item3':
        menu_item = cart.item3
        cart.item3 = None
    elif item_number == 'item4':
        menu_item = cart.item4
        cart.item4 = None
    elif item_number == 'item5':
        menu_item = cart.item5
        cart.item5 = None

    # If the menu item exists, increase its quantity by 1
    if menu_item:
        menu_item.quantity += 1
        menu_item.save()
        messages.warning(request, f"{menu_item.item_name} removed from cart for student {student.first_name}")
    messages.warning(request, f" ")
    cart.save()
    return render(request, 'order_staff.html', {'student': student , 'menu_items': menu_itemsall , 'carts':cartall})

def checkout_staff(request):
    if request.method == 'POST':
        # Get student information
        student = get_object_or_404(Student, pk=student_id)
        cart_items = Cart.objects.filter(studentid=student_id)
        total_amount = Decimal(request.POST.get('total_amount'))
    
                # Check if student has enough balance
        if student.virtual_wallet_balance < total_amount:
            messages.error(request, f"{student.first_name} has Insufficient balance ")
            return redirect('/order_staff/')

        # Store order information
        order_items = []
        for item in cart_items:
            for i in range(1, 6):
                menu_item = getattr(item, 'item{}'.format(i))
                if menu_item:
                    order_items.append(menu_item)

        order_time = timezone.now()
        order_mode = 'offline'

        # Create order object
        order = Order.objects.create(
            studentid=student,
            item1=order_items[0] if len(order_items) > 0 else None,
            item2=order_items[1] if len(order_items) > 1 else None,
            item3=order_items[2] if len(order_items) > 2 else None,
            item4=order_items[3] if len(order_items) > 3 else None,
            item5=order_items[4] if len(order_items) > 4 else None,
            total_amount=total_amount,
            order_time=order_time,
            order_mode=order_mode
        )
        

         # Create transaction
        transaction_type = 'debit'
        transaction_amount = total_amount
        transaction = Transaction.objects.create(
            student_id=student,
            transaction_type=transaction_type,
            transaction_amount=transaction_amount
        )

        # Update student wallet balance
        student.virtual_wallet_balance -= total_amount
        student.save()

        # Empty cart
        cart_items.delete()
        return receipt_staff(request, order.orderid)
    
def receipt_staff(request, orderid):
    order = Order.objects.get(pk=orderid)
    
    items = []
    for i in range(1, 6):
        item_field = f"item{i}"
        if getattr(order, item_field):
            menu_item = MenuItem.objects.get(pk=getattr(order, item_field).menuid)
            item_name = menu_item.item_name
            item_price = menu_item.price
            item_quantity = 1
            
            # Check if the item already exists in the list
            for item in items:
                if item['name'] == item_name:
                    item['quantity'] += 1
                    item['price'] += item_price
                    item_quantity = item['quantity']
                    break
            
            # If the item doesn't exist, add it to the list
            else:
                item = {
                    'name': item_name,
                    'price': item_price,
                    'quantity': item_quantity,
                }
                items.append(item)
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'receipt_staff.html', context)

def order_history_staff(request):
    order_type = request.POST.get('order_type') # get the order type from query parameter
    if order_type == '1':
        orders = Order.objects.filter(order_mode='online').order_by('-order_time')
    elif order_type == '2':
        orders = Order.objects.filter(order_mode='offline').order_by('-order_time')
    elif order_type == '3':
        orders = Order.objects.all().order_by('-order_time')
    else:
        orders = Order.objects.filter(order_mode='offline').order_by('-order_time')
    
    # Calculate number of items for each order
    for order in orders:
        student = Student.objects.get(pk=order.studentid_id )
        order.student_name = student.first_name + ' ' + student.last_name
        items = [order.item1, order.item2, order.item3, order.item4, order.item5]
        order.num_items = sum(1 for item in items if item is not None)
    context = {
        'orders': orders,
        'order_type': order_type,
    }
    
    return render(request, 'order_history_staff.html', context)

def reviews(request):
    feedbacks = Feedback.objects.all().order_by('-submission_time')
    total_reviews = feedbacks.count()
    positive_reviews = feedbacks.filter(rating__gte=4).count()
    neutral_reviews = feedbacks.filter(rating=3).count()
    negative_reviews = feedbacks.filter(rating__lte=2).count()
    
    for feedback in feedbacks:
        student = Student.objects.get(pk=feedback.studentid_id)
        menu = MenuItem.objects.get(pk=feedback.itemid_id)
        feedback.student_name = f'{student.first_name} {student.last_name}'
        feedback.item_name = f'{menu.item_name}'
    
    context = {
        'feedbacks': feedbacks,
        'total_reviews': total_reviews,
        'positive_reviews': positive_reviews,
        'neutral_reviews': neutral_reviews,
        'negative_reviews': negative_reviews,
    }
    
    return render(request, 'reviews.html', context)
