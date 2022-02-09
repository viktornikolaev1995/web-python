import base64
import json
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views import View
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Item, Review


class ItemForm(forms.Form):
    title = forms.CharField(label='Наименование товара', min_length=1, max_length=64)
    description = forms.CharField(label='Описание товара', min_length=1, max_length=1024)
    price = forms.IntegerField(label='Цена товара', min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    grade = forms.IntegerField(label='Оченка отзыва', min_value=1, max_value=10)
    text = forms.CharField(label='Текст отзыва', min_length=1, max_length=1024)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""
    def post(self, request):

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
        else:
            return HttpResponse('', status=401)

        if request.user.is_staff:
            pass
        else:
            return HttpResponse('', status=403)

        try:
            data = json.loads(request.body)
            form = ItemForm(data)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                price = form.cleaned_data['price']
                if title.isdigit() or description.isdigit():
                    return HttpResponse('400 - запрос не прошел валидацию', status=400)
                if price is None:
                    return HttpResponse('400 - запрос не прошел валидацию', status=400)
                obj = Item.objects.create(title=title, description=description, price=price)
                return JsonResponse({"id": obj.id}, status=201)
            else:
                return HttpResponse('400 - запрос не прошел валидацию', status=400)
        except json.JSONDecodeError:
            return HttpResponse('400 - json errors', status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""
    def post(self, request, item_id):
        try:
            data = json.loads(request.body)
            form = ReviewForm(data)
            if form.is_valid():
                text = form.cleaned_data['text']
                grade = form.cleaned_data['grade']
                if text.isdigit():
                    return HttpResponse('400 - запрос не прошел валидацию', status=400)
                if grade is None:
                    return HttpResponse('400 - запрос не прошел валидацию', status=400)
                try:
                    item_obj = Item.objects.get(pk=item_id)
                except ObjectDoesNotExist:
                    return HttpResponse('404 - товара с таким id не существует', status=404)
                rev_obj = Review.objects.create(grade=grade, text=text, item_id=item_obj.id)
                return JsonResponse({"id": rev_obj.id}, status=201)
            else:
                return HttpResponse('400 - запрос не прошел валидацию', status=400)
        except json.JSONDecodeError:
            return HttpResponse('400 - json errors', status=400)


class GetItemView(View):
    """View для получения информации о товаре. Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    @staticmethod
    def get_review_data(rev_objs):
        reviews = []
        for rev_obj in rev_objs:
            data = {
                'id': rev_obj.id,
                'text': rev_obj.text,
                'grade': rev_obj.grade
            }
            reviews.append(data)
        return reviews

    def get(self, request, item_id):
        try:
            item_obj = Item.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse('404 - товара с таким id не существует', status=404)
        rev_objs = Review.objects.filter(item_id=item_obj.id).order_by('id')
        reviews = []
        if len(rev_objs) > 5:
            rev_objs = Review.objects.filter(item_id=item_obj.id).order_by('-id')[:5]
            reviews = self.get_review_data(rev_objs)
        elif 1 <= len(rev_objs) <= 5:
            reviews = self.get_review_data(rev_objs)
        data = {
            'id': item_obj.id,
            'title': item_obj.title,
            'description': item_obj.description,
            'price': item_obj.price,
            'reviews': reviews
                }
        return JsonResponse(data, status=200, json_dumps_params={'ensure_ascii': False})
