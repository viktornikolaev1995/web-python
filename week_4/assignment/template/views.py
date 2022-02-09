from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

"""
тестирование get запросов
response = requests.get('http://127.0.0.1:8000/template/echo/', 
params={'a': 5, 'b': 100, 'c': 200, 'd': 400}, headers={'X-Print-Statement': 'test'}
)

response = requests.get('http://127.0.0.1:8000/template/echo/', 
params={'a': 5, 'b': 100, 'c': 200, 'd': 400}, 
)
тестирование post запросов
response = requests.post('http://127.0.0.1:8000/template/echo/', 
data={'a': 5, 'b': 100, 'c': 200, 'd': 400}, 
headers={'X-Print-Statement': 'test'}
)

response = requests.post('http://127.0.0.1:8000/template/echo/', 
data={'a': 5, 'b': 100, 'c': 200, 'd': 400}
)

тестирование неразрешенного put запроса
response = requests.put('http://127.0.0.1:8000/template/echo/', 
params={'a': 5, 'b': 100, 'c': 200, 'd': 400}, 
headers={'X-Print-Statement': 'test'}
)
"""


@csrf_exempt
def echo(request):
    context = {}
    statement = request.META.get('HTTP_X_PRINT_STATEMENT', 'empty')
    if request.method in ['GET', 'POST']:
        if request.method == 'GET':
            data = request.GET
            method = 'get '
        else:
            data = request.POST
            method = 'post '
        result = ''
        for key, value in data.items():
            result += ''.join(key) + ': ' + ''.join(value) + ' '
        response = method + result + f'statement is {statement}'
        context['response'] = response
        return render(request, 'echo.html', context=context)
    else:
        return HttpResponse(status=405)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
