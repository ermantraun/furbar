from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from . import models
from django.db.models import F
from django.utils import timezone

def index(request):
    start_date = timezone.now()
    end_date = start_date + timedelta(days=7)
    
    expiring_discounts = models.Discount.objects.filter(exiration_date__range=(start_date, end_date))
    print(expiring_discounts.all())
    return render(request, "furbar/index.html", )

def profile(request):
    return HttpResponse("This is the profile page")

def basket(request):
    pass

def basket_add(request):
    pass

def basket_delete(request):
    pass

def wishlist(request):
    pass

def wishlist_add(request):
    pass

def wishlist_delete(request):
    pass

def mailing(request):
    pass

def about(request):
    return HttpResponse("This is the about page")

def shop(request):
    return HttpResponse("This is the shop page")

def product(request, article):
    return(HttpResponse(article))

def blog(request):
    return HttpResponse("This is the blog page")

def contacts(request):
    return HttpResponse()