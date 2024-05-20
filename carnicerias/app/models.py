from datetime import date
from datetime import datetime
import email
from enum import unique
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(AbstractUser):
    #Extiende la clase AbstractUser por defecto de Django...

    #redefinimos username para hacerlo unique.
    username = models.CharField(
        unique=True,
        error_messages={
            'unique': 'Nombre de usuario no disponible.'
        },max_length=50)
    #El nivel de usuario nos indicara si se trata de un cliente (1), un usuario con permisos(2), o un administrador(3).
    user_level = models.IntegerField(blank=True, default = 1)        
    #redefinimos el field email de la clase usser para validar que el email sea unico.
    email = models.EmailField(
        unique=True,
        error_messages={
             'unique': 'Esta dirección de correo electrónico ya está siendo usada por otra cuenta.'
         }
    )
    #pip install django-phonenumber-field[phonenumbers]   or  pip install django-phonenumber-field[phonenumberslite], edit settings py 
    phone = PhoneNumberField()

    #REQUIRED_FIELDS = ['first_name','last_name','email'] 

    def __str__(self):
        return self.username

class Product(models.Model):
    """ if piece is True the product will be in units, 
    """
    name =  models.CharField(unique=True,max_length=40)
    description = models.CharField(max_length=100)
    piece = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    line = models.CharField(max_length=30)
    supplier = models.CharField(max_length=30)
    url_media = models.URLField()

    def __str__(self):
        return self.nombre

class Promotions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.DecimalField(decimal_places=2, max_digits=6)
    #regalo_compra = models.ForeignKey()
    #
    final_price = models.DecimalField(decimal_places=2, max_digits=4) 
    url_media = models.URLField()

    def __str__(self):
        return self.id  

