from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import *
from decimal import Decimal
from django.contrib import messages
from io import BytesIO
from PIL import Image
import numpy as np
from django.utils.html import format_html
import cv2
from django.utils import timezone
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
import face_recognition
from django.http import JsonResponse,Http404
from django.core.files.base import ContentFile
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def profile(request):
    user_id = request.session.get('studentid')
    student = Student.objects.get(studentid=user_id)
    context = {'student': student} 
    return render(request,'profile.html',context)
def login_view(request):
    return render(request,'login.html')

def ewallet(request):
    
    user_id = request.session.get('studentid')
    student = Student.objects.get(studentid=user_id)
    context = {'student': student} 
    return render(request,'ewallet.html',context)

def add_fund(request):
    if request.method == 'POST':
        student_id = request.session.get('studentid')
        amount = request.POST.get('transaction_amount')
        transaction_type = 'credit'
        student = Student.objects.get(studentid=student_id)
        student.virtual_wallet_balance += Decimal(amount)
        student.save()

        transaction = Transaction(
        student_id=student,
        transaction_type=transaction_type,
        transaction_amount=float(amount),
        transaction_time=timezone.now()
            )
        transaction.save()
        messages.success(request, format_html('Added <strong>₹{}</strong> to your virtual wallet balance.', amount))
        context = {'student': student} 
        return redirect('/ewallet/')

    

def update_profile(request):
    user_id = request.session.get('studentid')
    student = Student.objects.get(studentid=user_id)
    # return HttpResponse(request.session.get('studentid'))
    if not user_id:
        return redirect('login_view')
    
    if request.method == 'POST':
        student.studentid = request.POST.get('studentid')
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.mobileno = request.POST.get('mobileno')
        student.department_name = request.POST.get('department_name')
        student.semester = request.POST.get('semester')
        student.dob = request.POST.get('dob')
        student.gender = request.POST.get('gender')
        student.address = request.POST.get('address')
        student.save()
        messages.success(
                    request, f'Profile updated')
        return redirect('/profile/')
    
    return render(request, 'profile.html')



def loginuser(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        if (Student.objects.filter(email=useremail, password=password)).exists():
            user_details = Student.objects.get(email=useremail, password=password)
            user_id = user_details.studentid
            user_email = user_details.email
            request.session['studentid'] = user_id
            request.session['email'] = user_email
            # messages.success(request, 'Login successful!')
            return render(request, 'index.html', {'studentid': user_id})
        elif useremail == 'staff@gmail.com' and password == 'staff':
            request.session['email'] = useremail
            return render(request, 'index_staff.html')
        else:
            return HttpResponse("<script>alert('Invalid Email or Password');window.location='/login_view';</script>")


   
def index(request):
    return render(request,'index.html')

def indexstaff(request):
    return render(request,'index_staff.html')

def reg(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        # Perform basic form validation
        if not studentid or not first_name or not email or not password or not confirm_password:
            return HttpResponse("<script>alert('All fields are Required');window.location='/login_view';</script>")

        if password != confirm_password:
            return HttpResponse("<script>alert('Password don't match');window.location='/login_view';</script>")

        # Check if student with the same ID or email already exists
        if Student.objects.filter(studentid=studentid).exists():
            return HttpResponse("<script>alert('A student with the same ID already exists');window.location='/login_view';</script>")

        if Student.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('A student with the same email already exists');window.location='/login_view';</script>")
            

        # Create a new student object and save it to the database
        student = Student(studentid=studentid, first_name=first_name, email=email, password=password)
        student.save()

        # Redirect to a success page or login page
        return HttpResponse("<script>alert('Signup Completed');window.location='/login_view';</script>")


    else:
        return render(request, 'login.html')

def update_pass(request):
    studentid = request.session.get('studentid')
    if studentid:
        student = Student.objects.get(studentid=studentid)
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if student.password == old_password:
                if new_password == confirm_password:
                    student.password = new_password
                    student.save()
                    messages.success(request, 'Password updated successfully!')
                    return redirect('/profile/')
                else:
                    messages.error(request, 'New password and confirm password did not match!')
                    return redirect('/profile/')
            else:
                messages.error(request, 'Old password is incorrect!')
                return redirect('/profile/')
        
    else:
        return redirect('login')

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        image_data = request.POST['imagedata']
        # Decode the base64-encoded image data
        image_data = base64.b64decode(image_data.split(',')[1])

        # create an in-memory binary stream from the decoded image data
        stream = BytesIO(image_data)

        # create a PIL Image object from the binary stream
        img = Image.open(stream)


        # get the student object from the session
        student_id = request.session.get('studentid')
        student = Student.objects.get(pk=student_id)

        # check if the student already has an image saved
        try:
            old_student_image = StudentImage.objects.get(studentid=student)
            old_student_image.delete()
        except StudentImage.DoesNotExist:
            pass

        # create a new StudentImage object and save it to the database
        student_image = StudentImage(studentid=student, image=image_data)
        student_image.save()

        messages.success(
                    request, f'Image Saved Successfully')
        return redirect('/profile/')
    else:
        return HttpResponse('wrong user name or password or account does not exist!!')

def menushowstudent(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_student.html', {'menu_items': menu_items})

def add_to_cart(request, item_id):
    try:
        menu_item = MenuItem.objects.get(menuid=item_id)
    except MenuItem.DoesNotExist:
        raise Http404('Menu item not found')

    # Check if the student is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')

    # Get the student object
    student_id = request.session.get('studentid')
    student = Student.objects.get(pk=student_id)

    # Check if the student already has a cart
    cart, created = Cart.objects.get_or_create(studentid=student)

    # Check if the cart already contains the maximum number of items
    if cart.item1 and cart.item2 and cart.item3 and cart.item4 and cart.item5:
        messages.warning(request, 'The cart already contains the maximum number of items')
        return redirect('/menushowstudent/')

    # Add the selected item to the cart
    if not cart.item1:
        cart.item1 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f'{menu_item.item_name} added to cart')
    elif not cart.item2:
        cart.item2 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f'{menu_item.item_name} added to cart')
    elif not cart.item3:
        cart.item3 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f'{menu_item.item_name} added to cart')
    elif not cart.item4:
        cart.item4 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f'{menu_item.item_name} added to cart')
    elif not cart.item5:
        cart.item5 = menu_item
        menu_item.quantity -= 1
        messages.success(request, f'{menu_item.item_name} added to cart')

    cart.save()
    menu_item.save()

    return redirect('/menushowstudent/')


def viewcart(request):
    # Get the student object
    student_id = request.session.get('studentid')
    student = Student.objects.get(pk=student_id)

    # Get the cart items for the student
    cart_items = Cart.objects.filter(studentid=student)

    # Create a list to store the menu item details for each cart item
    cart_item_details = []

    # Loop through the cart items and fetch the related menu item details
    for item in cart_items:
        item_details = {
            'cartid': item.cartid,
            'item1': None,
            'item2': None,
            'item3': None,
            'item4': None,
            'item5': None,
        }

        if item.item1:
            item_details['item1'] = MenuItem.objects.get(menuid=item.item1.menuid)

        if item.item2:
            item_details['item2'] = MenuItem.objects.get(menuid=item.item2.menuid)

        if item.item3:
            item_details['item3'] = MenuItem.objects.get(menuid=item.item3.menuid)

        if item.item4:
            item_details['item4'] = MenuItem.objects.get(menuid=item.item4.menuid)

        if item.item5:
            item_details['item5'] = MenuItem.objects.get(menuid=item.item5.menuid)

        cart_item_details.append(item_details)

    context = {
        'cart_item_details': cart_item_details,
    }

    return render(request, 'cart.html', context)


def remove_item_from_cart(request, cart_id, item_number):
    cart = Cart.objects.get(cartid=cart_id)

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

    cart.save()
    return HttpResponse("<script>alert('Item Removed');window.location='/viewcart';</script>")


def checkout(request):
    if request.method == 'POST':
        # Get student information
        student_id = request.session.get('studentid')
        student = Student.objects.get(pk=student_id)
        password = request.POST.get('password')

        # Check student password
        if password != student.password:
            return HttpResponse("<script>alert('Incorrect Password');window.location='/viewcart';</script>")
            

        # Get cart information
        cart_items = Cart.objects.filter(studentid=student_id)
        total_amount = Decimal(request.POST.get('total_amount'))

        # Check if student has enough balance
        if student.virtual_wallet_balance < total_amount:
            return HttpResponse("<script>alert('Insufficient balance');window.location='/viewcart';</script>")

        # Store order information
        order_items = []
        for item in cart_items:
            for i in range(1, 6):
                menu_item = getattr(item, 'item{}'.format(i))
                if menu_item:
                    order_items.append(menu_item)

        order_time = timezone.now()
        order_mode = 'online'

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
        return receipt(request, order.orderid)

    return render(request, 'checkout.html')


def receipt(request, order_id):
    order = Order.objects.get(pk=order_id)
    
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
    return render(request, 'receipt.html', context)


def order_history_student(request):
    user_id = request.session.get('studentid')
    student = Student.objects.get(studentid=user_id)
    orders = Order.objects.filter(studentid=student).order_by('-order_time')
    
    # Calculate number of items for each order
    for order in orders:
        items = [order.item1, order.item2, order.item3, order.item4, order.item5]
        order.num_items = sum(1 for item in items if item is not None)

    context = {'orders': orders}
    return render(request, 'order_history_student.html', context)

def feedbackmenu(request):
    student_id = request.session.get('studentid')
    orders = Order.objects.filter(studentid=student_id)
    items = []
    for order in orders:
        items += [order.item1, order.item2, order.item3, order.item4, order.item5]
    # remove duplicates
    items = list(set(filter(None, items)))
    return render(request, 'feedback.html', {'items': items})

def add_feedback(request, item_id):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        student_id = request.session.get('studentid')
        item = MenuItem.objects.get(pk=item_id)
        
        # create a new Feedback object and save it
        feedback = Feedback.objects.create(
            studentid=Student.objects.get(pk=student_id),
            itemid=item,
            comment=comment,
            rating=rating,
            submission_time=timezone.now()
        )
        feedback.save()

        return redirect('/feedbackmenu/')
    else:
        # if request is not a POST request, render the feedback form
        item = MenuItem.objects.get(pk=item_id)
        context = {'item': item}
        return render(request, 'feedback.html', context)