from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from employeeData import settings

class Address(models.Model):
    houseNumber = models.CharField(max_length=50,null=True)
    street = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=250,null=True)
    
    def __str__(self):
        return self.city

    
class Experience(models.Model):
    companyName = models.CharField(max_length = 100,null=True)
    fromDate = models.CharField(max_length=10,null=True)
    toDate = models.CharField(max_length=10,null=True)
    #address = models.OneToOneField(Address, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=255,null=True)
    
    def __str__(self):
        return self.companyName

    

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

class Qualifications(models.Model):
    qualificationName = models.CharField(max_length=255,null=True)
    fromDate = models.CharField(max_length=10,null=True)
    toDate = models.CharField(max_length=10,null=True,)
    percentage = models.FloatField(validators=PERCENTAGE_VALIDATOR,null=True)
    
    def __str__(self):
        return self.qualificationName
    
class Projects(models.Model):
    title =  models.TextField(null=True)
    description =  models.TextField(null=True)
    
    def __str__(self):
        return self.title
    
class User(AbstractBaseUser):
    regid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False)
    email = models.EmailField(null=False,blank=False,unique=True)
    age =  models.IntegerField(null=True)
    genderChoices = (
    ("M", "Male"),
    ("F", "Female"),
    ("T", "Transgender"),
    ("NA", "Not Disclosed"),)
    password = None
    last_login = None
    gender =  models.CharField(max_length = 2,choices = genderChoices)
    phoneNumber = PhoneNumberField(null=False, blank=False, unique=False,)
    addressDetails = models.OneToOneField(Address, on_delete=models.CASCADE,null=True)
    workExperience = models.OneToOneField(Experience, on_delete=models.CASCADE,null=True) # multiple employee, list of dict
    qualifications = models.OneToOneField(Qualifications, on_delete=models.CASCADE,null=True) # multiple qualifications, list of dict
    projects = models.OneToOneField(Projects, on_delete=models.CASCADE,null=True) # multiple qualifications, list of dict
    photo = models.ImageField(upload_to ='uploads/',null=True)
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.name
    
