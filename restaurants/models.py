from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator


class Restaurant(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    opening_time = models.IntegerField()
    closing_time = models.IntegerField()

    #class Meta:
        #app_label = 'tablebooking'
        #db_table = 'restaurant'
        #managed = True
        #abstract = False


class Table(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE
    )
    size = models.IntegerField(
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])

    #class Meta:
     #   app_label = 'tablebooking'
      #  managed = True


class Booking(models.Model):
    table = models.ForeignKey(Table,
        on_delete=models.CASCADE)
    people = models.IntegerField()
    booking_date_time_start = models.DateTimeField()
    booking_date_time_end = models.DateTimeField()

    #class Meta:
     #   app_label = 'tablebooking'
      #  managed = True

class UserManager(BaseUserManager):
    def create_user(self, staffnumber, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not staffnumber:
            raise ValueError('Users must have a staff number')

        user = self.model(
            staffnumber=staffnumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, staffnumber, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            staffnumber,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, staffnumber, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            staffnumber,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in the New Manager to our Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=False,
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    staffnumber = models.CharField(unique=True, max_length=4, validators=[RegexValidator(regex=r'^\d{4}$', message='Staff number Length has to be exactly 4', code='nomatch')])

    objects = UserManager()
    # notice the absence of a "Password field", that is built in.
    EMAIL_FIELD = None
    USERNAME_FIELD = 'staffnumber'
    REQUIRED_FIELDS = [staffnumber] # Email & Password are required by default.



    def __str__(self):
        return self.staffnumber


