
from django.urls import path, include
from . import views


basket = [
    path('', views.basket, name='basket'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/', views.basket_delete, name='basket_delete'),
]

wishlist = [
    path('', views.wishlist, name='wishlist'),
    path('add/', views.wishlist_add, name='wishlist_add'),
    path('delete/', views.wishlist_delete, name='wishlist_delete'),
]

profile = [
    path('', views.profile, name='profile'),
]

shop = [
    path('', views.shop, name='shop'),
    path('product/<int:article>', views.product, name='product-details')
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include(profile), name='profile'),
    path('about/', views.about, name='about'),
    path('shop/', include(shop)),
    path('blog/', views.blog, name='blog'),
    path('contacts/', views.contacts, name='contacts'),
    path('basket/', include(basket)),
    path('wishlist/', include(wishlist)),
    path('mailing/', views.mailing, name='mailing'),
    
]


