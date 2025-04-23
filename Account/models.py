from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission, PermissionsMixin

# Create your models here.
class ManagerUser(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        all_roles = CustomUser.RoleChoices.choices
        user.set_password(password)
        user.save(using=self._db)
        if (user.role in [value for value,label in all_roles]):
            group = Group.objects.get(name=user.role)
            user.groups.add(group)
            user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):  
    class RoleChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        LECTURER = 'lecturer', 'Lecturer'
        STUDENT = 'student', 'Student'
    username = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    birth = models.DateField()
    mssv = models.CharField(max_length=10, default='', null=False, blank=False)
    role = models.CharField(max_length=50, choices=RoleChoices.choices, default='', null=False, blank=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = ManagerUser()
    
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name', 'phone_number', 'birth','role']
    USERNAME_FIELD = 'email'
    def has_perm(self, perm, obj=None):
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    