from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from datetime import timedelta


def dtime():
    return timezone.now() + timedelta(hours=3)

# department model
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    deleted = models.BooleanField(default = False)
    objects = models.Manager()

    def __str__(self):
        return str(self.name)
    

# custom user model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, fullname, department, password = None, is_admin = False):
        if not username:
            raise ValueError("The username field must be set")
        if not fullname:
            raise ValueError("The fullname field must be set")
        if department is None:
            raise ValueError("The department field must be set")
        
        user = self.model(
            username = username,
            fullname = fullname,
            department = department,
            is_admin = is_admin,
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, fullname, department, password = None):
        user = self.create_user(
            username = username,
            fullname = fullname,
            department = department,
            password = password,
            is_admin = True,
        )
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key = True)
    regdate = models.DateTimeField(default=dtime)
    username = models.CharField(unique = True, max_length = 150)
    fullname = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, default='M')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    phone = models.CharField(max_length=32, null=True, default=None)
    password_changed = models.BooleanField(default = False)
    last_login = models.DateTimeField(null = True, default=None)
    blocked = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    comment = models.TextField(null=True, default=None)
    deleted = models.BooleanField(default = False)
    groups = models.ManyToManyField(Group, blank = True, related_name = 'custom_users')
    user_permissions = models.ManyToManyField(Permission, blank = True, related_name = 'custom_users')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname', 'department']
    
    def __str__(self):
        return str(self.fullname)