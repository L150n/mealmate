from django.db import models
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
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


    
class StudentImage(models.Model):
    faceid = models.AutoField(primary_key=True)
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.BinaryField()

    def save(self, *args, **kwargs):
        if not self.faceid:
            # Auto-increment faceid
            last_record = StudentImage.objects.last()
            if last_record:
                self.faceid = last_record.faceid + 1
            else:
                self.faceid = 1
        super(StudentImage, self).save(*args, **kwargs)

class MenuItem(models.Model):
    menuid = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='images',  default='') 