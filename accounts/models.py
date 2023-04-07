from django.db import models

# Create your models here.

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    studentid = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    virtual_wallet_balance = models.DecimalField(max_digits=8, decimal_places=2,default=00.00)
    department_name = models.CharField(max_length=50)
    semester = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    dob = models.DateField(default='2000-01-01')
    address = models.CharField(max_length=200,default='None')
    mobileno = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StudentEncoding(models.Model):
    encoding_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    encoding_data = models.TextField()