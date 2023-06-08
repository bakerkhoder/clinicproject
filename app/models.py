from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User

# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('Users must have an email address')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self.create_user(username, password, **extra_fields)
#
#
# class User(AbstractUser):
#     username = models.CharField(unique=True, max_length=25)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     REQUIRED_FIELDS = []
#     USERNAME_FIELD = 'username'
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name = "User"
#         verbose_name_plural = "Users"
#         db_table = 'User'


class Patient(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        db_table = 'Patient'


class Doctor(models.Model):
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        db_table = 'Doctor'


class Nurse(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Nurse"
        verbose_name_plural = "Nurses"
        db_table = 'Nurse'


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    appoint_date = models.DateField()
    appoint_time = models.TimeField()
    treatment = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.treatment

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        db_table = 'Appointment'
