from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from uuid import uuid4
from django.core.exceptions import ValidationError

def upload_file_path(instance, file_name):
    ext = file_name.split('.')[-1]
    directory = instance.content_type.model
    name = uuid4().hex
    file_path = '{}/{}.{}'.format(directory, name, ext)
    return file_path

class CustomUserManager(UserManager):
    def create_user(self, **kwargs):
        basket = Basket()
        wishlist = WishList()
        basket.save()
        wishlist.save()
        kwargs['basket'] = basket
        kwargs['wishlist'] = wishlist
        user = super().create_user(**kwargs)
        return user

    def create_superuser(self, **kwargs):
        basket = Basket()
        wishlist = WishList()
        basket.save()
        wishlist.save()
        kwargs['basket'] = basket
        kwargs['wishlist'] = wishlist
        user = super().create_superuser(**kwargs)
        return user

class GenericOneToOne(GenericForeignKey):
    many_to_one = False
    one_to_many = False
    one_to_one = True
    
class User(AbstractUser, CustomUserManager):
    objects = CustomUserManager()
    country = models.CharField(max_length=120, default='', blank=True)
    city = models.CharField(max_length=120, default='', blank=True) 
    street_name = models.CharField(max_length=120, default='', blank=True)
    postcode = models.CharField(max_length=20, default='', blank=True)  
    additional_address_details = models.CharField(max_length=500, default='', blank=True)  
    phone_number = models.CharField(max_length=20, default='', blank=True)
    wishlist = models.OneToOneField("WishList", on_delete=models.CASCADE)
    basket = models.OneToOneField("Basket", on_delete=models.CASCADE)
    images = GenericRelation("Image")
    
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

class Discount(models.Model):
    value = models.SmallIntegerField()
    expiration_date = models.DateField()
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericOneToOne() 

class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    article = models.CharField(max_length=50, unique=True)
    categories = models.ManyToManyField(Category)
    Discount = GenericRelation("Discount")
    comments = GenericRelation("Comments")
    images = GenericRelation("Image")
    
    @property
    def first_image(self):
        return self.images.all()[0]

class Rating(models.Model):
    vote_count = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    @property
    def average_rating(self):
        return self.rating // self.vote_count
    
class WishList(models.Model):
    products = models.ManyToManyField(Product)

class Basket(models.Model):
    products = models.ManyToManyField(Product, through="BasketProduct")
    @property
    def cost(self):
        cost = 0
        for product in self.products.all():
            cost += product.price
        return cost   
         
class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()

class Comments(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateField(auto_now_add=True)
    rating = models.SmallIntegerField()
    text = models.TextField(default='')
    images = GenericRelation("Image")


class Order(models.Model):
    date = models.DateField(auto_now_add=True)
    cost = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120) 
    street_name = models.CharField(max_length=120, default='')
    postcode = models.CharField(max_length=20, default='')  
    additional_address_details = models.CharField(max_length=500, default='')  
    phone_number = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through="OrderProduct")

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()

class Image(models.Model):
    image = models.ImageField(upload_to=upload_file_path)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    
class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)

class Article(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    comments = GenericRelation("Comments")
    images = GenericRelation("Image")
    
    @property
    def first_image(self):
        return self.images.all()[0]
class MailingList(models.Model):
    email = models.EmailField()
    
