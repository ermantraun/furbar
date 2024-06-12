from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from . import models

@receiver(post_save, sender=models.Supply)
def increase_product_availability(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.quantity_available += instance.quantity
        product.save()

@receiver(post_save, sender=models.Comment)
def increase_product_availability(sender, instance, created, **kwargs):
    if created:
        c_type = instance.content_type
        obj_id = instance.object_id
        obj = c_type.get_object_for_this_type(pk=obj_id)

        rating, vote_count = obj.calculate_rating()
        obj.rating = rating
        obj.vote_count = vote_count
        obj.save()
        
@receiver(post_save, sender=models.Sale)
def reduce_product_availability(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.quantity_available -= instance.quantity
        product.save()
    
