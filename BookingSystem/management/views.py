from django.shortcuts import render

# Create your views here.

def request(request):
    
    return render(request, template_name='request.html')
