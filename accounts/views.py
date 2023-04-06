from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
def profile(request):
    return render(request,'profile.html')
def login_view(request):
    return render(request,'login.html')

def update_profile(request):
    # check if user is logged in
    if 'id' in request.session and 'email' in request.session:
        # retrieve student details from database
        student = Student.objects.get(studentid=request.session['id'], email=request.session['email'])
        
        # if request method is POST, update student details
        if request.method == 'POST':
            # retrieve updated details from form
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
            student.save()  # save changes to database
            return redirect('profile')  # redirect to profile page after update
        
        # if request method is GET, display student details
        return render(request, 'profile.html', {'student': student})
    
    # if user is not logged in, redirect to login page
    return redirect('login_view')
def loginuser(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        if (Student.objects.filter(email=useremail, password=password)).exists():
            user_details = Student.objects.get(email=useremail, password=password)
            user_id = user_details.studentid
            user_email = user_details.email
            request.session['id'] = user_id
            request.session['email'] = user_email
            return render(request, 'index.html')
        
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