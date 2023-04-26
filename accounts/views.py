from django.shortcuts import render,redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
import face_recognition
from django.http import JsonResponse
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
    
    return render(request, 'ewallet.html')

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
        context = {'student': student} 
        messages.success(
                    request, f'Profile updated')
        return render(request,'profile.html',context)
    
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
                    context = {'student': student} 
                    return render(request,'profile.html',context)
                else:
                    messages.error(request, 'New password and confirm password did not match!')
                    context = {'student': student} 
                    return render(request,'profile.html',context)
            else:
                messages.error(request, 'Old password is incorrect!')
                context = {'student': student} 
                return render(request,'profile.html',context)
        
    else:
        return redirect('login')

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        data = request.POST['imagedata']
        format, imgstr = data.split(';base64,') 
        ext = format.split('/')[-1] 
        image_data = imgstr.encode('utf-8')
        image_data = base64.b64decode(image_data)

        # create an in-memory binary stream from the decoded image data
        stream = BytesIO(image_data)

        # create a PIL Image object from the binary stream
        img = Image.open(stream)

        # save the PIL Image object to a bytes object
        img_bytes = BytesIO()
        img.save(img_bytes, format=ext)

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
        student_image = StudentImage(studentid=student, image=img_bytes.getvalue())
        student_image.save()

        messages.success(
                    request, f'Image Saved Successfully')
        context = {'student': student} 
        return render(request,'profile.html',context)
    else:
        return HttpResponse('wrong user name or password or account does not exist!!')

def menushowstudent(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'menu_student.html', {'menu_items': menu_items})