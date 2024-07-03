from django.contrib import admin
from . import models

from django.contrib import admin



admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Manufacturer)
admin.site.register(models.ProductTag)
admin.site.register(models.Product)
admin.site.register(models.WishList)
admin.site.register(models.Supply)
admin.site.register(models.Sale)
admin.site.register(models.Basket)
admin.site.register(models.Buy)
admin.site.register(models.Comment)
admin.site.register(models.HouseOrder)
admin.site.register(models.TakeAwayOrder)
admin.site.register(models.OrderProduct)
admin.site.register(models.ArticleTag)
admin.site.register(models.Article)
admin.site.register(models.Discount)
admin.site.register(models.UserImage)
admin.site.register(models.ProductImage)
admin.site.register(models.CommentImage)
admin.site.register(models.ArticleImage)
admin.site.register(models.CategoryImage)
admin.site.register(models.Coupon)
admin.site.register(models.WareHouse)