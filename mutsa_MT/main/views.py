from django.shortcuts import render

# Create your views here.
def intropage(request):
    return render(request, 'main/intro.html')

def firstPage(request):
    return render(request, 'main/firstPage.html')