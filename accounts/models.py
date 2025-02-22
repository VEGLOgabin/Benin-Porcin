from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,AbstractUser


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, password, email, phone_number, address, role, profile_picture=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        if not role:
            raise ValueError('Users must have a role')

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            is_staff=False, 
            is_admin=False,
            **kwargs
        )

        # Set the profile picture if provided
        if profile_picture:
            # Resize the image using Pillow
            img = Image.open(profile_picture)
            img = img.resize((300, 300), Image.ANTIALIAS)  # Resize to 300x300
            img_io = BytesIO()  # Create a BytesIO object to save the resized image
            img.save(img_io, format='JPEG', quality=75)  # Save the resized image
            img_io.seek(0)  # Rewind the file pointer
            user.profile_picture.save(profile_picture.name, ContentFile(img_io.read()), save=False)
        else:
            # Set a default profile picture if none is provided
            default_image_path = 'profiles/default.png'
            if default_storage.exists(default_image_path):
                with default_storage.open(default_image_path, 'rb') as f:
                    user.profile_picture.save(default_image_path, ContentFile(f.read()), save=False)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, first_name, last_name, password, email, phone_number, address, role, profile_picture=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            password=password,
            profile_picture=profile_picture,
            is_staff=True,
            is_admin=False
        )
        return user
    
    def create_superuser(self, first_name, last_name, email, password, phone_number, address, role, profile_picture=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            role=role,
            password=password,
            profile_picture=profile_picture,
            is_staff=True,
            is_admin=True
        )
        return user



class ActiveUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('breeder', 'Breeder'),
        ('veterinarian', 'Veterinarian'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', "phone_number", "address", "role"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'ActiveUser'






class BreederProfile(models.Model):
    user = models.OneToOneField(ActiveUser, on_delete=models.CASCADE, related_name='breeder_profile')
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_size = models.IntegerField(help_text="Number of pigs")
    description = models.TextField(blank=True, null=True)


class VeterinarianProfile(models.Model):
    user = models.OneToOneField(ActiveUser, on_delete=models.CASCADE, related_name='veterinarian_profile')
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField()
    specialization = models.CharField(max_length=255, blank=True, null=True)
    availability = models.BooleanField(default=True)


class BuyerProfile(models.Model):
    user = models.OneToOneField(ActiveUser, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=255, blank=True, null=True)
    interest = models.TextField(help_text="What kind of pigs/products they are looking for")



from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(ActiveUser, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

class BreederProfile(Profile):
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_size = models.IntegerField(help_text="Number of pigs", validators=[MaxValueValidator(10000)])

class VeterinarianProfile(Profile):
    license_number = models.CharField(max_length=100, unique=True)
    experience_years = models.IntegerField(validators=[MaxValueValidator(50)])
    specialization = models.CharField(max_length=255, blank=True, null=True)
    availability = models.BooleanField(default=True)

class BuyerProfile(Profile):
    company_name = models.CharField(max_length=255, blank=True, null=True)
    interest = models.TextField(help_text="What kind of pigs/products they are looking for")

# Automatically create profile based on user role
@receiver(post_save, sender=ActiveUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'breeder':
            BreederProfile.objects.create(user=instance)
        elif instance.role == 'veterinarian':
            VeterinarianProfile.objects.create(user=instance)
        elif instance.role == 'buyer':
            BuyerProfile.objects.create(user=instance)