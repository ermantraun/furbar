from .models import Basket, WishList, Product
def shop(get_response):
    
    def middleware(request):

        if not request.user.is_authenticated:
            
            basket = request.session.get('basket')
            
            wishlist = request.session.get('wishlist')
            
            if basket is None:
                basket = Basket()
                basket.save()
                request.session['basket'] = basket.id
            else:
                basket = Basket.objects.get(id=basket)

            if wishlist is None:
                wishlist = WishList()
                wishlist.save()
                request.session['wishlist'] = wishlist.id
            else:
                wishlist = WishList.objects.get(id=wishlist)
            
            request.user.basket = basket
            request.user.wishlist = wishlist
            request.user.buy = None
        else:
            ...
            #user already have basket and wishlist
            
        
        
        
        response = get_response(request)



        return response
    
    return middleware