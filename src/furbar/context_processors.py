

def base_html_template_context(request):
    basket = request.user.basket.products.all()
    wishlist = request.user.wishlist.products.all()
    return {'basket': basket, 'wishlist': wishlist, 'basket_products_count': len(basket)}