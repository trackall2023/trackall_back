from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.


SEXE_CHOICES = (
    ("HOMME", "HOMME"),
    ("FEMMME", "FEMME"),
    ("AUCUN", "AUCUN")
)


class MyUserManger(BaseUserManager):
    def create_user(self, lastname, firstname, password=None, birth_date=timezone.now(), sexe='', adresse='', description='', profession='', telephone=''):
        """
        Creates and saves a User with the given email, name and password.
        """
        user = self.model(
            lastname=lastname,
            firstname=firstname,
            birth_date=birth_date,
            adresse=adresse,
            description=description,
            profession=profession,
            telephone=telephone,
            sexe=sexe

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, lastname, firstname, password=None, birth_date=timezone.now(), sexe='', adresse='', description='', profession='', telephone=''):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(
            password=password,
            lastname=lastname,
            firstname=firstname,
            birth_date=birth_date,
            sexe=sexe,
            adresse=adresse,
            description=description,
            profession=profession,
            telephone=telephone

        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class Custom_User(AbstractUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email adress', max_length=255, default="")
    lastname = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    sexe = models.CharField(max_length=15, choices=SEXE_CHOICES, default="AUCUN")
    telephone = models.CharField(max_length=20,unique= True)
    picture = models.ImageField(default="default.png",  upload_to='statics/')

    birth_date = models.DateField(default=timezone.now)
    adresse= models.CharField(max_length=200, default="")
    description = models.CharField(max_length=200, default="Aucune description")
    profession = models.CharField(max_length=200, default="Aucune rofession")
    date_created_at = models.DateTimeField(auto_now_add=True)
    date_updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)


    objects = MyUserManger()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return f"{self.lastname} {self.firstname}"

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
        # Simplest possible answer: All admins are staff
        return self.is_admin
