
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('blog/', views.blog, name='blog'),
    path('contacts/', views.contacts, name='contacts'),
]
