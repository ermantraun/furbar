from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .apps import FurbarConfig
from django import apps
import json
def parse_params(request, params_names, method='GET'):
    params = {}
    if method == 'GET':
        data_source = request.GET
    elif method == 'POST':
        data_source = request.POST
    else:
        raise ValueError("Unsupported method. Only 'GET' and 'POST' are supported.")

    for name in params_names:
        if name.endswith('[]'):
            if name in data_source:
                params[name] = data_source.getlist(name)
        else:
            if name in data_source:
                params[name] = data_source.get(name)
    
    return params

def base_common_validator(params):
    return params
def validate_params(params, validators, common_validator=base_common_validator):

    for key, value in params.items():
        if key in validators:
            
            if not(validators[key](value)) and value:
                print(key, value)
                return False

    if not common_validator(params):
        return False
    
    return True

def is_convertible_to_number(number):
    try:
        int(number)
        return True
    except ValueError:
        return False



def get_paginator(objects, page_number, per_page, page_button_range):
    if page_button_range % 2 == 0:
        raise ValueError('“page_button_range” must be an odd number')

    paginator = Paginator(objects, per_page)
    if paginator.num_pages < page_number:
        page_number = 1
    
    page = paginator.page(page_number)
        
    if page.has_next():
        next_page = page.next_page_number()
    else:
        next_page = False
        
    if page.has_previous():
        previous_page = page.previous_page_number()
    else:
        previous_page = False
        
    if page.number % page_button_range == 0:
        
        left_page_button_range = []
        right_page_button_range = [page_number for page_number in range(page_number + 1, page_number + page_button_range)]
    
    else:
        left_page_button_range = [page_number for page_number in range(page_number - (page_button_range // 2), page_number)]
        right_page_button_range = [page_number for page_number in range(page_number + 1, page_number + (page_button_range // 2) + 1)]
    
    left_page_button_range = filter(lambda page_number: page_number > 0, left_page_button_range)
    right_page_button_range = filter(lambda page_number: page_number <= paginator.num_pages, right_page_button_range)
    
    first_page_number = 1
    last_page_number = paginator.num_pages
    
    
    return page, next_page, previous_page, first_page_number, last_page_number, left_page_button_range, right_page_button_range, page_number
    

def index(request):

    expiring_discounts_products, no_expiring_discounts = models.Discount.get_expiring_discounts(models.Product, limit=15)
    bestsellers = models.Sale.get_bestsallers(limit=15)
    random_categories = models.Category.get_random_categories(limit=4)
    latest_articles = models.Article.get_latest_articles(limit=6)
    return render(request, "furbar/index.html", 
                  context={'expiring_discounts_products': expiring_discounts_products,
                           'no_expiring_discounts': no_expiring_discounts,
                           'bestsellers': bestsellers,
                           'random_categories': random_categories,
                           'latest_articles':latest_articles})

def profile(request):
    return HttpResponse("This is the profile page")

def login(request):
    return HttpResponse("This is the login page")

def register(request):
    return HttpResponse("This is the register page")

def basket(request):
    
    return render(request, "furbar/basket.html", context={
        
    })

def basket_add(request, article):
    

    product = get_object_or_404(models.Product, article=article)
    if product not in request.user.basket.products.all():
        request.user.basket.products.add(product)
    return redirect('basket')

def basket_delete(request, article):
    

    product = get_object_or_404(models.Product, article=article)
    if product in request.user.basket.products.all():
        request.user.basket.products.remove(product)
    return redirect('basket')

def empty_basket(request):
    request.user.basket.products.clear()
    return redirect('basket')
def wishlist(request):
    
    
    
    return render(request, 'furbar/wishlist.html', context = {
        
    })

def wishlist_add(request, article):
    product = get_object_or_404(models.Product, article=article)
    if product not in request.user.wishlist.products.all():
        request.user.wishlist.products.add(product)
    return redirect('wishlist')

def wishlist_delete(request, article):
    product = get_object_or_404(models.Product, article=article)
    if product in request.user.wishlist.products.all():
        request.user.wishlist.products.remove(product)
    return redirect('wishlist')

def empty_wishlist(request):
    request.user.wishlist.products.clear()
    return redirect('wishlist')

def mailing(request):
    pass

def about(request):
    return HttpResponse("This is the about page")

def category_filter_query(products, category_name):
    products = products.filter(category__name=category_name)
    return products

def manufacturer_filter_query(products, manufacturer_name):

    products = products.filter(manufacturer__name=manufacturer_name)
    return products

def tags_filter_query(products, tags):
    filtered_products = products.filter(tags__name__in=tags).distinct()
    

    
    return filtered_products

def min_price_filter_query(products, min_price):
    products = products.filter(price__gte=int(min_price))
    return products

def max_price_filter_query(products, max_price):
    products = products.filter(price__lte=int(max_price))
    return products


shop_params_validators = {
    'category': lambda category: isinstance(category, str) and category,
    'manufacturer': lambda manufacturer: isinstance(manufacturer, str) and manufacturer,
    'tags': lambda tags: isinstance(tags, list),
    'min_price': lambda min_price: is_convertible_to_number(min_price) and int(min_price) >= 0,
    'max_price': lambda max_price: is_convertible_to_number(max_price) and int(max_price) >= 0,
    'sort_by': lambda sort_by: isinstance(sort_by, str) and sort_by in ['price', 'rating', 'sales', 'default'],
    'sort_order': lambda sort_order: isinstance(sort_order, str) and sort_order in ['asc', 'desc', 'default'],
    'page': lambda page: is_convertible_to_number(page)
}

shop_filters_queries = {
    'category': category_filter_query,
    'manufacturer': manufacturer_filter_query,
    'tags[]': tags_filter_query,
    'min_price': min_price_filter_query,
    'max_price': max_price_filter_query,
}

def common_shop_params_validator(params):
    if 'min_price' in params and 'max_price' in params:
        if params['min_price'] >= params['max_price']:
            return False


    return True


def get_filtered_products(products, filters, filters_queris):
    for filters_name, filters_value in filters.items():
        if filters_name in filters_queris and filters_value != 'All':
            
            products = filters_queris[filters_name](products, filters_value)
    return products



def shop(request):
    all_products = models.Product.objects.all()
    categories = models.Category.objects.all()
    manufacturers = models.Manufacturer.objects.all()
    tags = models.ProductTag.objects.all()
    all_products_count = models.Product.objects.count()
    per_page = 10
    page_button_range = 5
    page_number = 1
    sort_by = 'rating'
    sort_order = 'asc'
    products = all_products
    products_count = all_products_count
    category = None
    page = 1
    params_names = ['category','manufacturer', 'tags[]','min_price','max_price','sort_by', 'sort_order', 'page']
    if request.GET:
        params = parse_params(request, params_names, 'GET')
        if params:
            if not validate_params(params, shop_params_validators, common_shop_params_validator):
                return HttpResponseBadRequest('Неверный запрос')
            
            if 'page' in params: 
                page_number = int(params['page'])
                del params['page']
        
            if 'sort_by' in params:
                sort_by = params['sort_by']
                del params['sort_by']
          
            if 'sort_order' in params:
                sort_order = params['sort_order']
                del params['sort_order']
       
            if 'category' in params and category != 'All':
                category = params['category']
                if category != 'All':
                    category = models.Category.objects.get(name=params['category'])
        
            if params:
                product_filters = params
                
                products = get_filtered_products(all_products, product_filters, shop_filters_queries)
                
                products_count = products.count()

    products = models.Product.sort(products, sort_by, sort_order)
    page, next_page, previous_page, first_page_number, last_page_number, left_page_button_range, right_page_button_range, page_number = get_paginator(products, page_number, per_page, page_button_range)
    products = page.object_list

    
    return render(request, "furbar/shop.html", {
        'categories': categories,
        'manufacturers': manufacturers,
        'tags': tags,
        'all_products_count': all_products_count,
        'find_products_count': products_count,
        'products': products,
        'category': category,
        'next_page': next_page,
        'previous_page': previous_page,
        'first_page_number': first_page_number,
        'last_page_number': last_page_number,
        'page_number': page_number,
        'left_page_button_range': left_page_button_range,
        'right_page_button_range': right_page_button_range,
    })


def add_comment(request):
    if request.method == 'POST':
        model_name = request.POST.get('model').split()[0].lower()
        obj_id = request.POST.get('obj_id')
        if model_name is not None and obj_id is not None:
            c_type = get_object_or_404(ContentType, model=model_name, app_label=FurbarConfig.name)
            model = apps.apps.get_model(FurbarConfig.name, model_name)
            obj = get_object_or_404(model, id=obj_id)
            
            if request.method == 'POST' and obj.comments_allowed(request.user):
                vote = request.POST.get('vote')
                if vote:
                    vote = int(vote[0])
                    if vote >= 1 and vote <= 5:
                        vote = int((vote / 5) * 100)
                        text = request.POST.get('text', '')
                        
                        images = request.FILES.getlist('images[]', [])
                        
                        
                        comment = models.Comment(content_type=c_type, object_id=obj_id, user=request.user, 
                                        vote=vote, text=text)
                        comment.save()
                        
                        if images:
                            for image in images[0:4]:

                                models.CommentImage(comment=comment, large=image).save()
                        
                        response = {
                            "username": request.user.username,
                            "username_image": request.user.image.preview.url,
                            "date": comment.date.strftime('%B %d, %Y'),
                            "vote": comment.vote,
                            "comment_id": comment.id,
                            "text": comment.text,
                            "images_url": [{'preview_url': image.preview.url, 'large_url': image.large.url} 
                                        for image in comment.images.all()]
                            
                        }
                        return JsonResponse(response, status=200)
            
    return JsonResponse(status=400)

def edit_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        text = request.POST.get('text')
        if comment_id is not None and text is not None:
            comment = get_object_or_404(models.Comment, id=comment_id)
            if comment.edit_allowed(request.user):
                comment.text = text
                comment.save()
                return JsonResponse({'text': text}, status=200)
            
    return JsonResponse(status=400)
def del_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        if comment_id is not None:
            comment = get_object_or_404(models.Comment, id=comment_id)
            if comment.edit_allowed(request.user):
                comment.delete()
                
                return JsonResponse({}, status=200)
            
    return JsonResponse(status=400)

def calculate_delivery_cost(postal_code):
    return 1000

def check_delivery_cost(request):
    if request.method == 'GET':
         postal_code = request.GET.get('postal_code')
         if postal_code is not None:
             try:
                 postal_code = int(postal_code)
             except ValueError:
                 return JsonResponse(status=400)
             
             return JsonResponse({'cost':calculate_delivery_cost(postal_code)}, status=200)

            
    return JsonResponse(status=400)

def check_coupon(request):
    
    if request.method == 'GET':
        coupon = request.GET.get('coupon')
        cost = request.GET.get('cost')
        
        try:
            cost = int(cost)
        except ValueError:
            return JsonResponse(status=400)
        
        if coupon is not None and cost is not None:
            
            try:
                coupon = models.Coupon.objects.get(pk=coupon)
            except models.Coupon.DoesNotExist:
                return JsonResponse(status=400)
            
            if coupon.is_valid():
                if coupon.is_persent_discount:

                    discount = (cost // 100) * coupon.discount_amount
                    return JsonResponse({'discount': discount, 'couponCode': coupon.code}, status=200)
                else:
                    return JsonResponse({'discount': coupon.discount_amount, 'couponCode': coupon.code}, status=200)
            else:
                return JsonResponse(status=400)
            
            
    return JsonResponse(status=400)


def validate_order_products(products):
    products = json.loads(products)
    
    if isinstance(products, list):
        for product in products:
            if isinstance(product, dict):
                article = product.get('article')
                quantity = product.get('quantity')
                if not ((article is not None and is_convertible_to_number(article)) and \
                    (quantity is not None and is_convertible_to_number(quantity))):
                        return False
            else:
                return False
    return True
        

order_params_validators = {
    'delivery': lambda delivery: delivery in ['takeaway', 'house'],
    'products': validate_order_products
    
}

def logout(request):
    pass

def get_order_products(products):
    products_instances = []
    for product in products:
        article = int(product['article'])
        quantity = int(product['quantity'])
        
        product = get_object_or_404(models.Product, article=article)
        
        if product.quantity_available < quantity:
            return HttpResponseBadRequest('Недостаточно на складе товара: ' + product.name + '<br>' +
                                        'Вы запросили: ' + str(quantity) + '<br>' +
                                        'На складе: ' + str(product.quantity_available) + '<br>' +
                                        'Пожалуйста, попробуйте заказать позднее')
        
        products_instances.append({'product': product, 'quantity': quantity})
    return products_instances

def get_order_final_cost(products):
    final_cost = 0
    for product in products:
        final_cost += product['product'].price * product['quantity']
    return final_cost
def order(request):
    if request.method != 'POST' :
        return HttpResponseBadRequest('Неверный запрос')
    
    
    if not (models.Order.ordering_allowed(request.user)):
        return redirect('login')
    
    products = request.POST.get('products', '[{}]')
    delivery = request.POST.get('delivery', None)
    coupon = request.POST.get('coupon', None)
    
    if not validate_params({'products': products, 'delivery': delivery}, order_params_validators):
        return HttpResponseBadRequest('Неверный запрос')
    
    products = get_order_products(json.loads(products))
    
    if isinstance(products, HttpResponseBadRequest):
        return products
        
    final_cost = get_order_final_cost(products)
    

    if delivery == 'house':
        payment_types = models.HouseOrder.PERMENT_TYPE_CHOISES
        warehouses = None
    else:
        payment_types = models.TakeAwayOrder.PERMENT_TYPE_CHOISES
        warehouses = models.WareHouse.objects.all()
        
    return render(request, 'furbar/order.html', {'products': products, 'final_cost': final_cost, 
                                                 'delivery':delivery, 'coupon': coupon, 
                                                 'payment_types': payment_types, 'warehouses': warehouses})


def check_required_params_present(request_params, order_params):
    missing_params = [param for param, required in order_params.items() if required and param not in request_params]
    return missing_params
def place_order(request):
    general_params_required = {
    'first_name': True,
    'last_name': True,
    'country': False,  
    'phone': True,
    'email': True,
    'delivery': True,
    'products': True,  
    'payment_type': True,
    }

    house_delivery_params_required = {
        'street': True,
        'apartment': False,  
        'city': True,
        'postcode': True
    }

    takeaway_delivery_params_required = {
        'warehouse': True
    }

    
    
    params = json.loads(request.body)


    delivery = params.get('delivery', '')
    
    if delivery == 'house':
        full_params_required = {**general_params_required, **house_delivery_params_required}
        
        
    elif delivery == 'warehouse': 
        full_params_required = {**general_params_required, **takeaway_delivery_params_required}
        
    elif delivery == '':
 
        return JsonResponse({}, status=400)
    
    for param, isRequired  in full_params_required.items():
            if isRequired and param not in params:
                return JsonResponse({}, status=400)
            else:
                print(True)
    
    return JsonResponse({}, status=200)

def product(request, article):
    
    product = get_object_or_404(models.Product, article=article)
    user_comments = models.Comment.getUserComments(product, request.user)
    comments_allowed = product.comments_allowed(request.user)
    related_products = product.related_products(15)
    
    return render(request, "furbar/product-details.html", {
        'product':product,
        'user_comments': user_comments,
        'comments_allowed': comments_allowed,
        'related_products': related_products
    })



def blog(request):
    return HttpResponse("This is the blog page")

def contacts(request):
    return HttpResponse()