
from django.urls import path, include
from . import views


basket = [
    path('', views.basket, name='basket'),
    path('add/<int:article>', views.basket_add, name='basket_add'),
    path('delete/<int:article>', views.basket_delete, name='basket_delete'),
]

wishlist = [
    path('', views.wishlist, name='wishlist'),
    path('add/<int:article>', views.wishlist_add, name='wishlist_add'),
    path('delete/<int:article>', views.wishlist_delete, name='wishlist_delete'),
]

profile = [
    path('', views.profile, name='profile'),
]

shop = [
    path('', views.shop, name='shop'),
    path('product/<int:article>', views.product, name='product-details'),
]

blog = [
    path('', views.blog, name='blog'),
    path('<int:article>', views.blog, name='article')
]

comment = [
    path('add/', views.add_comment, name='add_comment'),
    path('edit/', views.edit_comment, name='edit_comment'),
    path('del/', views.del_comment, name='del_comment'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include(profile), name='profile'),
    path('about/', views.about, name='about'),
    path('shop/', include(shop)),
    path('blog/', include(blog), name='blog'),
    path('contacts/', views.contacts, name='contacts'),
    path('basket/', include(basket)),
    path('wishlist/', include(wishlist)),
    path('mailing/', views.mailing, name='mailing'),
    path('comment/', include(comment), name='')
    
]


