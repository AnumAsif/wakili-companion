from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return render(request, 'court-list/index.html') 

def cause_list(request):
    return render(request, 'court-list/causelist.html')    