from django.db import models
from django.utils import timezone
from django.contrib.auth.models  import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
import datetime






class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email, 
            password=password,
            is_staff = True
        )
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff = True,
            is_admin = True
        )
        
        user.save(using=self._db)
        return user


    ...

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    first_Name = models.CharField(max_length=255 )
    last_Name = models.CharField(max_length=255)
    regNo = models.CharField(max_length=20)
    #dateOfBirth = models.DateField(null=True)
    status = models.CharField(max_length=23, choices =(('Student','Student'), ('Alumin', 'Alumin')))
    #contact = models.CharField(max_length=15)
    # notice the absence of a "Password field", that is built in.

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.first_Name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

Halls = [
    ('Kulubya','Kulubya'),
    ('Nanziri','Nanziri'),
    ('Mandella','Mandella'),
    ('Pearl','Pearl'),
    ('North Hall','North Hall')
]
    

Maritial_status =[
    ('Married','Married'),
    ('Single','Single')

]
    

nextofkin =[
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('brother', 'brother'),
    ('Sister', 'Sister'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Other', 'Other')

]
    



year_choices = [(r,r) for r in range(1989, datetime.date.today().year+1)]




class Basicinfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yearOfEntry =  models.IntegerField(('year'),choices=year_choices, default=datetime.datetime.now().year)
    course = models.CharField(max_length=120)
    homeAddress = models.CharField(max_length=150)
    nextOfKin = models.CharField(max_length=150, blank=True)
    relationship = models.CharField(max_length=150,choices = nextofkin)
    contactNOK = models.CharField(max_length=15, blank=True)
    maritialStatus = models.CharField(max_length=15 ,choices=Maritial_status )
    contact = models.CharField(max_length=20)
    DoB = models.DateField(null=True)
    gender = models.CharField(max_length=15, choices =(('Male','Male'), ('Female','Female')))


    class Meta:
        abstract = True


class Alumin(Basicinfo):
    yrOfCompletion = models.IntegerField(('year'),choices=year_choices, default=datetime.datetime.now().year)
    positionHeldAtKyumsa = models.CharField('KYUMSA POSITION', max_length=100)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    jobDescription = models.CharField(max_length=200, null=True, blank=True)
    since = models.DateField()

    def __str__(self):
        return self.user.first_Name



class Student(Basicinfo):
    faculty = models.CharField(max_length=30)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    hall = models.CharField(max_length=233,choices=Halls)
    residenceStatus = models.CharField(max_length=50, choices=(('Resident','Resident'), ('Non-Resident','Non-Resident')))
    recentSch = models.CharField(max_length=255, null=True, blank=True)
    award = models.CharField(max_length=55, null=True, blank=True)
    respnosibilityHeld = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.first_Name