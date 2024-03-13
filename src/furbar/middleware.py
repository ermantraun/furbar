from .models import Basket, WishList, Product
def shop(get_response):
    
    def middleware(request):

        if not request.user.is_authenticated:
            
            basket = request.session.get('basket', None)
            
            wishlist = request.session.get('wishlist', None)
            
            if basket is None:
                basket = Basket()
                basket.save()
                request.session['basket'] = basket.id
            
            if wishlist is None:
                wishlist = WishList()
                wishlist.save()
                request.session['wishlist'] = wishlist.id
            
            
            request.user.basket = basket
            request.user.wishlist = wishlist
            
        else:
            ...
            #user already have basket and wishlist
            
        
        
        
        response = get_response(request)



        return response
    
    return middleware