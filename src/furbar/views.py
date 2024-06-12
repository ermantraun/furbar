from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from . import models
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from .apps import FurbarConfig
from django import apps
def parse_get_params(request, params_names):
    params = {}
    for name in params_names:
        if name.endswith('[]'):
            if name in request.GET:
                params[name] = request.GET.getlist(name)
        else:
            if name in request.GET:
                params[name] = request.GET.get(name)
    
    
    return params

def validate_params(params, validators, common_validator):

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

def basket(request):
    pass

def basket_add(request, article):
    

    product = get_object_or_404(models.Product, article=article)
    
    request.user.basket.products.add(product)
    return HttpResponse("ok")

def basket_delete(request, article):
    

    product = get_object_or_404(models.Product, article=article)
    
    request.user.basket.products.remove(product)
    return HttpResponse("ok")
def wishlist(request, article):
    pass

def wishlist_add(request, article):
    product = get_object_or_404(models.Product, article=article)
        
    request.user.wishlist.products.add(product)
    return HttpResponse("ok")

def wishlist_delete(request, article):
    product = get_object_or_404(models.Product, article=article)
    
    request.user.wishlist.products.remove(product)
    return HttpResponse("ok")
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
        params = parse_get_params(request, params_names)
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


def add_comment(request, model, obj_id):
    c_type = get_object_or_404(ContentType, model=model, app_label=FurbarConfig.name)
    model = apps.apps.get_model(FurbarConfig.name, model)
    obj = get_object_or_404(model, id=obj_id)
    
    if request.method == 'POST' and obj.commentsAllowed(request.user):
        vote = request.POST.get('vote')
        if vote:
            vote = int(vote[0])
            if vote >= 1 and vote <= 5:
                vote = int((vote / 5) * 100)
                text = request.POST.get('text')
                
                images = request.FILES.getlist('images[]')
                
                
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
                    "text": comment.text,
                    "images_url": [{'preview_url': image.preview.url, 'large_url': image.large.url} 
                                   for image in comment.images.all()]
                    
                }
                print(response)
                return JsonResponse(response)
            
    return JsonResponse({'status': 'fail'})


def product(request, article):
    
    product = get_object_or_404(models.Product, article=article)
    user_comments = request.user.getUserComments(product)
    commentsAllowed = product.commentsAllowed(request.user)
    
    return render(request, "furbar/product-details.html", {
        'product':product,
        'user_comments': user_comments,
        'commentsAllowed': commentsAllowed
    })



def blog(request):
    return HttpResponse("This is the blog page")

def contacts(request):
    return HttpResponse()