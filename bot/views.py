from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def test(request):
    # return HttpResponse('test food')
    return render(request, 'test.html', context={'TRACKING_ID':'UA-114588997-1'})