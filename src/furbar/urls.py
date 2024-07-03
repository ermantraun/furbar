
from django.urls import path, include
from . import views


basket = [
    path('', views.basket, name='basket'),
    path('add/<int:article>', views.basket_add, name='basket_add'),
    path('delete/<int:article>', views.basket_delete, name='basket_delete'),
    path('empty', views.empty_basket, name='empty_basket'),
]

wishlist = [
    path('', views.wishlist, name='wishlist'),
    path('add/<int:article>', views.wishlist_add, name='wishlist_add'),
    path('delete/<int:article>', views.wishlist_delete, name='wishlist_delete'),
    path('empty/<int:article>', views.empty_wishlist, name='wishlist_empty'),
]

profile = [
    path('', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout')
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
order = [
    path('', views.order, name='order'),
    path('place-order/', views.place_order, name='place_order'), 
    path('check-delivery-cost/', views.check_delivery_cost, name='check_delivery_cost'),
    path('check-coupon/', views.check_coupon, name='check_coupon'),

]
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include(profile)),
    path('about/', views.about, name='about'),
    path('shop/', include(shop)),
    path('blog/', include(blog)),
    path('contacts/', views.contacts, name='contacts'),
    path('basket/', include(basket)),
    path('wishlist/', include(wishlist)),
    path('mailing/', views.mailing, name='mailing'),
    path('comment/', include(comment),),
    path("order/", include(order)),

    
]


