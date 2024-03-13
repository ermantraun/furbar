from django.contrib import admin
from . import models



admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Manufacturer)
admin.site.register(models.Product)
admin.site.register(models.Rating)
admin.site.register(models.WishList)
admin.site.register(models.Basket)
admin.site.register(models.BasketProduct)
admin.site.register(models.Comments)
admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.Image)
admin.site.register(models.Tag)
admin.site.register(models.Article)