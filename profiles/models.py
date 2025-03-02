from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BiodataProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('Never Married', 'Never Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    height = models.FloatField(help_text="Height in cm")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES)
    
    # Personal Information
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50, blank=True)
    mother_tongue = models.CharField(max_length=50)
    
    # Education and Career
    education = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    annual_income = models.CharField(max_length=50)
    
    # Family Information
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    siblings = models.IntegerField(default=0)
    
    # Contact Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    
    # Additional Information
    about_me = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Biodata"
