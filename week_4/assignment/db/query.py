import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grader.settings")
import django
django.setup()

from datetime import datetime
from django.db.models import Q, Count, Avg
from pytz import UTC
from db.models import User, Blog, Topic

"""
тестирование
python
from db import query
query.create()
query.edit_all()
query.delete()
query.edit_u1_u2()
query.unsubscribe_u2_from_blogs()

from django.db import connection
connection.queries
connection.queries[-1]['sql']
"""

"""Создать пользователя first_name = u1, last_name = u1.

Создать пользователя first_name = u2, last_name = u2.

Создать пользователя first_name = u3, last_name = u3.

Создать блог title = blog1, author = u1.

Создать блог title = blog2, author = u1.

Подписать пользователей u1 u2 на blog1, u2 на blog2.

Создать топик title = topic1, blog = blog1, author = u1.

Создать топик title = topic2_content, blog = blog1, author = u3, created = 2017-01-01.

Лайкнуть topic1 пользователями u1, u2, u3."""


# def delete():
#     user_all = User.objects.all()
#     for user in user_all:
#         user.delete()
#     blog_all = Blog.objects.all()
#     for blog in blog_all:
#         blog.delete()
#     topic_all = Topic.objects.all()
#     for topic in topic_all:
#         topic.delete()


def create():
    """Создание объектов в базу"""
    user_u1 = User.objects.create(first_name='u1', last_name='u1')
    user_u1.save()
    user_u2 = User.objects.create(first_name='u2', last_name='u2')
    user_u2.save()
    user_u3 = User.objects.create(first_name='u3', last_name='u3')
    user_u3.save()
    user_u1 = User.objects.get(first_name='u1')
    user_u2 = User.objects.get(first_name='u2')
    user_u3 = User.objects.get(first_name='u3')
    blog1 = Blog.objects.create(title='blog1', author=user_u1)
    blog1.save()
    blog2 = Blog.objects.create(title='blog2', author=user_u1)
    blog2.save()
    blog1 = Blog.objects.get(title='blog1')
    blog1.subscribers.add(user_u1, user_u2)
    blog2 = Blog.objects.get(title='blog2')
    blog2.subscribers.add(user_u2)
    topic1 = Topic.objects.create(title='topic1', blog=blog1, author=user_u1)
    topic1.save()
    topic2 = Topic.objects.create(
        title='topic2_content',
        blog=blog1,
        author=user_u3,
        created=datetime(2017, 1, 1, tzinfo=UTC))
    topic2.save()
    topic1 = Topic.objects.get(title='topic1')
    topic1.likes.add(user_u1, user_u2, user_u3)


def edit_all():
    """Изменяет first_name на uu1 у всех пользователей"""
    user_all = User.objects.all()
    for user in user_all:
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    """Изменяет first_name на uu1 у пользователей, у которых first_name u1 или u2"""
    users_u1_u2 = User.objects.filter(Q(first_name='u1') | Q(first_name='u2'))
    for user in users_u1_u2:
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    """Удаляет пользователя с first_name u1"""
    user_u1 = User.objects.get(first_name='u1')
    user_u1.delete()


def unsubscribe_u2_from_blogs():
    """Отписывает пользователя с first_name u2 от блогов"""
    user_u2 = User.objects.get(first_name='u2')
    blog_all = user_u2.subscriptions.all()
    for blog in blog_all:
        blog.subscribers.remove(user_u2)
        blog.save()


def get_topic_created_grated():
    """Возвращает топики, у которых дата создания больше 2018-01-01"""
    query = Topic.objects.filter(created__gt=datetime(2018, 1, 1, tzinfo=UTC))
    return query


def get_topic_title_ended():
    """Возвращает топик, у которого title заканчивается на content"""
    query = Topic.objects.filter(title__iendswith='content')
    return query


def get_user_with_limit():
    """Возвращает первых 2х пользователей, сортирует в обратном порядке по id"""
    query = User.objects.all().order_by('-id')[:2]
    return query


def get_topic_count():
    """Возвращает количество топиков в каждом блоге, как topic_count, и сортирует по возрастанию по полю topic_count"""
    query = Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')
    return query


def get_avg_topic_count():
    """Возвращает среднее количество топиков в блоге"""
    query = Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))
    return query


def get_blog_that_have_more_than_one_topic():
    """Возвращает блоги, в которых топиков больше одного"""
    query = Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)
    return query


def get_topic_by_u1():
    """Возвращает все топики автора с first_name u1"""
    query = User.objects.get(first_name='u1').topic_set.all()
    return query


def get_user_that_dont_have_blog():
    """Возвращает пользователей, у которых нет блогов и сортирует результат по возрастанию по id"""
    query = User.objects.filter(blog__isnull=True).order_by('id')
    return query


def get_topic_that_like_all_users():
    """Возвращает топики, которые лайкнули все пользователи"""
    users = User.objects.all()
    topics = Topic.objects.filter(likes=users)
    return topics


def get_topic_that_dont_have_like():
    """Возвращает топики, у которых нет лайков"""
    topics = Topic.objects.filter(likes__isnull=True)
    return topics


