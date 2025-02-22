from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,AbstractUser

# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = [
        ('breeder', 'Breeder'),
        ('veterinarian', 'Veterinarian'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)



class BreederProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='breeder_profile')
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_size = models.IntegerField(help_text="Number of pigs")
    description = models.TextField(blank=True, null=True)


class VeterinarianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='veterinarian_profile')
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField()
    specialization = models.CharField(max_length=255, blank=True, null=True)
    availability = models.BooleanField(default=True)


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    interest = models.TextField(help_text="What kind of pigs/products they are looking for")

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    breeder = models.ForeignKey(BreederProfile, on_delete=models.CASCADE, related_name='consultations')
    veterinarian = models.ForeignKey(VeterinarianProfile, on_delete=models.CASCADE, related_name='consultations')
    symptoms = models.TextField()
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')



class PigListing(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    breeder = models.ForeignKey(BreederProfile, on_delete=models.CASCADE, related_name='pig_listings')
    breed = models.CharField(max_length=255)
    age_months = models.IntegerField()
    weight_kg = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='pigs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, related_name='transactions')
    pig_listing = models.ForeignKey(PigListing, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending')


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
