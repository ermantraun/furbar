from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


from django.core.exceptions import ValidationError

def spigot_validator(value):
    if not value:
        raise ValidationError()


validators = {
    'common': lambda x: x, 
    'user': {
        'country': [spigot_validator],
        'city': [spigot_validator],
        'street_name': [spigot_validator],
        'postcode': [spigot_validator],
        'phone_number': [spigot_validator],
    },
}

class User(AbstractUser):
    country = models.CharField(max_length=120, default='', validators=validators['user']['country'])
    city = models.CharField(max_length=120, default='',validators=validators['user']['city']) 
    street_name = models.CharField(max_length=120, default='',validators=validators['user']['street_name'])
    postcode = models.CharField(max_length=20, default='',validators=validators['user']['postcode'])  
    additional_address_details = models.CharField(max_length=500, default='')  
    phone_number = models.CharField(max_length=20, default='', validators=validators['user']['phone_number'])
    favorite_products = models.ManyToManyField("Product", through="FavoriteProducts")
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        if update_fields is not None:
            self.full_clean(exclude=update_fields)
        else:
            self.full_clean()
          
        super().save(force_insert=force_insert, force_update=force_update, 
                         using=using, update_fields=update_fields,)
User.email.validators = EmailValidator

#не забыть: добавить наследование категорий
class Categorie(models.Model):
    name = models.CharField(max_length=120, unique=True, )
    
    
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Product(models.Model):
    name = models.CharField(max_length=500, unique=True, validators=['Product']['name'])
    description = models.TextField(validators=['Product']['description'])
    price = models.PositiveIntegerField(validators=['Product']['price'])
    discount = models.SmallIntegerField(validators=['Product']['discount'])
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    article = models.GeneratedField(
        expression="SUBSTRING(MD5(CONCAT('product_', CAST(id AS CHAR))), 1, 8)",
        output_field=models.CharField(max_length=8, unique=True), 
    )
    categories = models.ManyToManyField(Categorie)
    reviews = models.ManyToManyField(User, through="ProductReview")
    
class Rating(models.Model):
    vote_count = models.PositiveIntegerField(validators=['Rating']['vote_count'])
    rating = models.PositiveIntegerField(validators=['Rating']['rating'])
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class FavoriteProduct(models.MOdel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()

class ProductReview(models.Model):
    product = models.ForeignKey(Product, onn_delete=models.CASCADE)
    user = models.ForeignKey(User, onn_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    text = models.TextField()
    