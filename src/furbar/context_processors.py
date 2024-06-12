

def base_html_template_context(request):
    basket = request.user.basket.products.all()
    wishlist = request.user.wishlist.products.all()
    buy = request.user.buy.products.all() if request.user.buy is not None else None
    return {'basket': basket, 'wishlist': wishlist, 'buy': buy, 'basket_products_count': len(basket)}