from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from uuid import uuid4
from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from imagekit.models import ProcessedImageField
from datetime import datetime, timedelta
from django.utils import timezone 
from random import sample
import string
import secrets


def upload_file_path(instance, file_name):
    ext = file_name.split('.')[-1]
    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day
    name = uuid4().hex
    file_path = '{}/{}/{}/{}.{}'.format(year, month, day, name, ext)
    return file_path


def generate_coupon_value(length=8):
    alphabet = string.ascii_uppercase + string.digits  # символы, используемые для генерации кода
    coupon_code = ''.join(secrets.choice(alphabet) for _ in range(length))  # случайный выбор символов
    return coupon_code


class CustomUserManager(UserManager):
    def create_user(self, **kwargs):
        basket = Basket()
        wishlist = WishList()
        buy = Buy()
        basket.save()
        wishlist.save()
        buy.save()
        kwargs['basket'] = basket
        kwargs['wishlist'] = wishlist
        kwargs['buy'] = buy
        user = super().create_user(**kwargs)
        return user

    def create_superuser(self, **kwargs):
        basket = Basket()
        wishlist = WishList()
        buy = Buy()
        basket.save()
        wishlist.save()
        buy.save()
        kwargs['basket'] = basket
        kwargs['wishlist'] = wishlist
        kwargs['buy'] = buy
        user = super().create_superuser(**kwargs)
        return user

class User(AbstractUser, CustomUserManager):
    objects = CustomUserManager()
    country = models.CharField(max_length=120, default='', blank=True)
    city = models.CharField(max_length=120, default='', blank=True) 
    street_name = models.CharField(max_length=120, default='', blank=True)
    postcode = models.CharField(max_length=20, default='', blank=True)  
    additional_address_details = models.CharField(max_length=500, default='', blank=True)  
    phone = models.CharField(max_length=20, default='', blank=True)
    wishlist = models.OneToOneField("WishList", on_delete=models.CASCADE)
    basket = models.OneToOneField("Basket", on_delete=models.CASCADE)
    buy = models.OneToOneField("Buy", on_delete=models.CASCADE, null=True)
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        
        if update_fields is not None:
            self.full_clean(exclude=update_fields)
        else:
            self.full_clean()
          
        super().save(force_insert=force_insert, force_update=force_update, 
                         using=using, update_fields=update_fields,)

        

class Category(models.Model):
    parent = models.OneToOneField("Category", on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120, unique=True)
    discount = GenericRelation("Discount")
    @property
    def products_count(self):
        products_count = len(self.products.all())
        return products_count
    
    @property
    def category_hierarchy(self):
        hierarchy = []
        parent = self.parent
        while parent:
            hierarchy.append(parent)
            parent = parent.parent
        hierarchy.reverse()
        
        return hierarchy
    
    @classmethod
    def get_random_categories(cls, limit):
        all_categories = cls.objects.all()
        
        if len(all_categories) <= limit:
            return all_categories
        

        random_categories = sample(list(all_categories), limit)
        return random_categories

    
    
class Manufacturer(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Discount(models.Model):
    value = models.SmallIntegerField()
    expiration_date = models.DateField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey() 
    
    class Meta:
        unique_together = [["object_id", "content_type"]]
    
    @classmethod
    def get_expiring_discounts(cls, ctype, limit):
        start_date = timezone.now()
        end_date = start_date + timedelta(days=7)
        ctype = ContentType.objects.get(model=ctype.__name__.lower())
        
        expiring_ctype_discounts = cls.objects.filter(expiration_date__range=(start_date, end_date), 
                                                            content_type=ctype)[0:limit]
        
        if not expiring_ctype_discounts:
            no_expiring_discounts = True
        else:
            no_expiring_discounts = False
            
        expiring_discounts_products = map(lambda discount: discount.content_object, expiring_ctype_discounts.all())
        
        return expiring_discounts_products, no_expiring_discounts
    

class Coupon(models.Model):
    code = models.CharField(max_length=8, unique=True, blank=True, default=generate_coupon_value, primary_key=True)
    discount_amount = models.SmallIntegerField()
    is_persent_discount = models.BooleanField(default=True)
    expiration_date = models.DateField()
    max_usage_quantity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    usage_quantity = models.IntegerField(null=True, blank=True)
    def coupon_expired(self):
        if self.expiration_date < timezone.now().date():
            return True
        else:
            return False

    def is_valid(self):
        if self.coupon_expired() or self.usage_quantity >= self.max_usage_quantity:
            return False
        
        return True
    
class ProductTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="products")
    article = models.GeneratedField(expression=models.F("price") * models.F("id"), output_field=models.IntegerField(), db_persist=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    tags = models.ManyToManyField(ProductTag, related_name="products")
    discount = GenericRelation("Discount")
    comments = GenericRelation("Comment")
    quantity_available = models.PositiveBigIntegerField()
    rating = models.IntegerField(default=0, blank=True)
    vote_count = models.PositiveIntegerField(default=0, blank=True)
    
    
    def related_products(self, count):
        tags = list(map(lambda x: x.name, self.tags.all()))
        related_products = Product.objects.filter(tags__name__in=tags).exclude(id=self.id)
        return related_products[0:count]
    
    def comments_allowed(self, user):
        if (user.is_authenticated and self in user.buy.products.all() and 
            self.comments.filter(user=user).count() < 1):
            return True
        else:
            return False
        
    def calculate_rating(self):
        vote_count = 0
        vote_sum = 0

        for comment in self.comments.all():
            vote_count += 1
            vote_sum += comment.vote
        
        if vote_count:
            
            return int(vote_sum / vote_count), vote_count
        
    @property
    def has_discount(self):
        if self.discounted_price is not None:
            return True
        else:
            return False
    
    @property
    def truncated_description(self):
        if len(self.description) > 20:
            return self.description[:20] + '...'
        
        return self.description

    
    @property 
    def discounted_price(self):
        product_discount = self.discount.all()
        category_discount = self.category.discount.all()
        if product_discount or category_discount:
            common_discount = (product_discount[0].value if product_discount else 0) + (category_discount[0].value 
                                                                                        if category_discount else 0)
            discounted_price = self.price * (100 - common_discount) // 100
            min_product_price = int(self.price * 0.30)
            
            if discounted_price > min_product_price:
                return discounted_price
            else:
                return min_product_price

    @property
    def first_image(self):
        try:
            return self.images.all()[0]
        except IndexError:
            return None
    

    @staticmethod
    def sort(products, sort_by, sort_order):
        products = products.annotate(models.Count('sales'))
        if sort_by is None:
            products = products.order_by('rating', 'sales', 'price')
        elif sort_by == "rating":
            products = products.order_by('rating', 'sales', 'price')
        elif sort_by == "price":
            products = products.order_by('price', 'rating', 'sales')
        elif sort_by == "sales":
            products = products.order_by('sales', 'rating', 'price')
            
        if sort_order == "desc":
            products = products.reverse()
        
        
        return products


    
     
class Supply(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supplies')
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField(default=0)
    total_revenue = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    
    @classmethod
    def get_bestsallers(cls, limit):

        
        date = timezone.now()
        week, month, year = date.isocalendar()[1], date.month, date.year
        all_sales = cls.objects.all()
        
        bestsellers_all_time = all_sales.values('product').annotate(total=models.Count('product')).order_by('-total')[0:limit]  
        bestsellers_month = all_sales.filter(date__year=year, date__month=month).values('product').annotate(total=models.Count('product')).order_by('-total')[0:limit]
        bestsellers_week = all_sales.filter(date__year=year, date__week=week).values('product').annotate(total=models.Count('product')).order_by('-total')[0:limit]
        
        
        
        return (map(lambda bestseller: Product.objects.get(pk=bestseller['product']), bestsellers_all_time), 
                map(lambda bestseller: Product.objects.get(pk=bestseller['product']), bestsellers_month), 
                map(lambda bestseller: Product.objects.get(pk=bestseller['product']), bestsellers_week))
        
class Buy(models.Model):
    products = models.ManyToManyField(Product)


class WishList(models.Model):
    products = models.ManyToManyField(Product)

class Basket(models.Model):
    products = models.ManyToManyField(Product)

    
    
    @property
    def cost(self):
        cost = 0
        for product in self.products.all():
            if product.has_discount:
                cost += product.discounted_price
            else:
                cost += product.price
        return cost   
    

class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    date = models.DateField(auto_now_add=True)
    vote = models.SmallIntegerField()
    text = models.TextField(default='')

    def edit_allowed(self, user):
        if user == self.user:
            return True
        else:
            return False

    @staticmethod 
    def getUserComments(ctype, user):
        if user.is_authenticated:
            return ctype.comments.filter(user=user)

class WareHouse(models.Model):
    city = models.CharField(max_length=120)
    additional_address = models.CharField(max_length=120)
    


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [('paid', 'paid'), ('unpaid', 'unpaid') ]
    
    date = models.DateField(auto_now_add=True)
    cost = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through="OrderProduct")
    notes = models.CharField(max_length=500, default='')
    payment_status = models.CharField(max_length=30, default='unpaid', choices=PAYMENT_STATUS_CHOICES)
    @staticmethod
    def ordering_allowed(user):
        if user.is_authenticated:
            return True
        else:
            return False


 
class HouseOrder(Order):
    PERMENT_TYPE_CHOISES = [('online', 'Оплата онлайн')] 
    
    country = models.CharField(max_length=120, default='')
    city = models.CharField(max_length=120, default='') 
    street_name = models.CharField(max_length=120, default='')
    postcode = models.CharField(max_length=20, default='')  
    additional_address_details = models.CharField(max_length=500, default='')  
    payment_type = models.CharField(max_length=30, default='online', choices=PERMENT_TYPE_CHOISES)



class TakeAwayOrder(Order):
    PERMENT_TYPE_CHOISES = [('online', 'Оплата онлайн'), ('on_receipt', 'Оплата при получении')]
    
    warehouse = models.OneToOneField(WareHouse, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=30, default='online', choices=PERMENT_TYPE_CHOISES)
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.SmallIntegerField()
    
class ArticleTag(models.Model):
    name = models.CharField(max_length=120, unique=True)

class Article(models.Model):
    name = models.CharField(max_length=250, unique=True)
    date = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(ArticleTag)
    text = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="articles")
    comments = GenericRelation("Comment")   
    rating = models.IntegerField(default=0, blank=True)
    vote_count = models.PositiveIntegerField(default=0, blank=True)
    
    def calculate_rating(self):
        vote_count = 0
        vote_sum = 0

        for comment in self.comments.all():
            vote_count += 1
            vote_sum += comment.vote
        
        if vote_count:
            
            return int(vote_sum / vote_count), vote_count
    
    @property
    def first_image(self):
        return self.images.all()[0]
    
    @classmethod
    def get_latest_articles(cls, limit):
        return cls.objects.all().order_by('-date')[0:limit]
    
class MailingList(models.Model):
    email = models.EmailField()
    
class ProductImage(models.Model):
    large = ProcessedImageField(upload_to=upload_file_path,
                                           processors=[SmartResize(570, 604)],
                                           format='JPEG',
                                           options={'quality': 100})
    preview = ImageSpecField(source='large',
                                      processors=[SmartResize(270, 303)],
                                      format='JPEG',
                                      options={'quality': 100})
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

class ArticleImage(models.Model):
    large = ProcessedImageField(upload_to=upload_file_path,
                                           processors=[SmartResize(770, 479)],
                                           format='JPEG',
                                           options={'quality': 100})
    preview = ImageSpecField(source='large',
                                      processors=[SmartResize(370, 230)],
                                      format='JPEG',
                                      options={'quality': 100})
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE,related_name="images")
    
class UserImage(models.Model):
    large = ProcessedImageField(upload_to=upload_file_path,
                                           processors=[SmartResize(770, 479)],
                                           format='JPEG',
                                           options={'quality': 100})
    preview = ImageSpecField(source='large',
                                      processors=[SmartResize(100, 100)],
                                      format='JPEG',
                                      options={'quality': 100})
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="image")

class CommentImage(models.Model):
    large = ProcessedImageField(upload_to=upload_file_path,
                                           processors=[SmartResize(770, 479)],
                                           format='JPEG',
                                           options={'quality': 100})
    preview = ImageSpecField(source='large',
                                      processors=[SmartResize(100, 100)],
                                      format='JPEG',
                                      options={'quality': 100})
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="images")

class CategoryImage(models.Model):
    large = ProcessedImageField(upload_to=upload_file_path,
                                           processors=[SmartResize(770, 479)],
                                           format='JPEG',
                                           options={'quality': 100})
    preview = ImageSpecField(source='large',
                                      processors=[SmartResize(480, 600)],
                                      format='JPEG',
                                      options={'quality': 100})
    
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="image")