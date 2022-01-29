from django.shortcuts import render

# Create your views here.


def home(request):
    # View for the home page
    return render(request, 'home.html')
