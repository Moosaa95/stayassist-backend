from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from accounts.manager import CustomUserManager, ProfileManager
from commons.mixins import ModelMixin

from cloudinary.models import CloudinaryField


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin, ModelMixin):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


class Profile(ModelMixin):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    profile_picture = CloudinaryField("image", null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    objects = ProfileManager()
