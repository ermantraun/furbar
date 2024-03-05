from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the home page")

def profile(request):
    return HttpResponse("This is the profile page")

def about(request):
    return HttpResponse("This is the about page")

def shop(request):
    return HttpResponse("This is the shop page")

def blog(request):
    return HttpResponse("This is the blog page")

def contacts(request):
    return HttpResponse("This is the contacts page")