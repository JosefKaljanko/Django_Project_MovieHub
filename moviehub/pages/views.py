from django.shortcuts import render

def home(request):
    """home page views"""
    return render(request, 'pages/home.html')

def about(request):
    """about page views"""
    return render(request, "pages/about.html")

def author(request):
    """Author page views"""
    return render(request, "pages/about_author.html")

