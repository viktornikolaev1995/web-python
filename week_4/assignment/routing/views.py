from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def simple_route(request):
    if request.method == 'GET':
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

# @csrf_exempt
def slug_route(request, slug):
    if request.method in ['GET', 'POST', 'PUT']:
        return HttpResponse(slug)
    else:
        return HttpResponse(status=405)

# @csrf_exempt
def sum_route(request, num1, num2):
    if request.method in ['GET', 'POST', 'PUT']:
        return HttpResponse(int(num1) + int(num2))
    else:
        return HttpResponse(status=400)


def sum_get_method(request):
    if request.method == 'GET':
        if request.GET.get('a') and request.GET.get('b'):
            try:
                a = int(request.GET.get('a'))
                b = int(request.GET.get('b'))
            except ValueError:
                return HttpResponse(status=400)
            return HttpResponse(int(a) + int(b))
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)


# @csrf_exempt
def sum_post_method(request):
    if request.method == 'POST':
        if request.POST.get('a') and request.POST.get('b'):
            try:
                a = int(request.POST.get('a'))
                b = int(request.POST.get('b'))
            except ValueError:
                return HttpResponse(status=400)
            return HttpResponse(int(a) + int(b))
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)








