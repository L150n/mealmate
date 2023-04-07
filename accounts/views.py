from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Student
from django.contrib.auth import authenticate, login
from django.contrib import messages


from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def profile(request):
    user_id = request.session.get('studentid')
    student = Student.objects.get(studentid=user_id)
    context = {'student': student} 
    return render(request,'profile.html',context)
def login_view(request):
    return render(request,'login.html')


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
            return render(request, 'index.html',{'studentid':user_id})
        
        else:
            return HttpResponse('wrong user name or password or account does not exist!!')
    return render(request, 'login.html')
   
def index(request):
    return render(request,'index.html')

def reg(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')


        # Perform basic form validation
        if not studentid or not first_name or not email or not password or not confirm_password:
            return render(request, 'login.html', {'error': 'All fields are required'})

        if password != confirm_password:
            return render(request, 'login.html', {'error': 'Passwords do not match'})

        # Check if student with the same ID or email already exists
        if Student.objects.filter(studentid=studentid).exists():
            return render(request, 'login.html', {'error': 'A student with the same ID already exists'})

        if Student.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'A student with the same email already exists'})

        # Create a new student object and save it to the database
        student = Student(studentid=studentid, first_name=first_name, email=email, password=password)
        student.save()

        # Redirect to a success page or login page
        return HttpResponseRedirect(reverse('success'))

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
            else:
                messages.error(request, 'Old password is incorrect!')
        return render(request, 'update_pass.html')
    else:
        return redirect('login')
