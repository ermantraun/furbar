from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import ValidationError


class User(AbstractUser):
    country = models.CharField(max_length=120, default='')
    city = models.CharField(max_length=120, default='') 
    street_name = models.CharField(max_length=120, default='')
    postcode = models.CharField(max_length=20, default='')  
    additional_address_details = models.CharField(max_length=500, default='')  
    phone_number = models.CharField(max_length=20, default='')
    favorite_products = models.ManyToManyField("Product", through="FavoriteProduct")
    images = GenericRelation("Image")
    images_size = models.CharField(max_length=30)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        if update_fields is not None:
            self.full_clean(exclude=update_fields)
        else:
            self.full_clean()
          
        super().save(force_insert=force_insert, force_update=force_update, 
                         using=using, update_fields=update_fields,)


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Manufacturer(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    discount = models.SmallIntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    article = models.CharField(max_length=50, unique=True)
    categories = models.ManyToManyField(Category)
    comments = GenericRelation("Comments")
    images = GenericRelation("Image")
    images_size = models.CharField(max_length=30)
    
class Rating(models.Model):
    vote_count = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()

class Comments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateField(auto_now_add=True)
    rating = models.SmallIntegerField()
    text = models.TextField()
    images = GenericRelation("Image")
    images_size = models.CharField(max_length=30)

class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    cost = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=120, default='')
    city = models.CharField(max_length=120, default='') 
    street_name = models.CharField(max_length=120, default='')
    postcode = models.CharField(max_length=20, default='')  
    additional_address_details = models.CharField(max_length=500, default='')  
    phone_number = models.CharField(max_length=20, default='')
    products = models.ManyToManyField(Product, through="OrderProduct")

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()

class Image(models.Model):
    name = models.CharField(max_length=120, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
class Tags(models.Model):
    name = models.CharField(max_length=120, unique=True)

class Article(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)
    text = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comments = GenericRelation("Comments")
    images = GenericRelation("Image")
    images_size = models.CharField(max_length=30)
