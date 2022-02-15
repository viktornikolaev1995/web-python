from __future__ import absolute_import, unicode_literals

import json
import requests
from celery import task
from django.core.exceptions import ObjectDoesNotExist

from .models import Setting

@task()
def smart_home_manager():
    try:
        bedroom_temperature = Setting.objects.get(controller_name='bedroom_temperature')
    except ObjectDoesNotExist:
        bedroom_temperature = None

    try:
        boiler_temperature = Setting.objects.get(controller_name='boiler_temperature')
    except ObjectDoesNotExist:
        boiler_temperature = None

    request = requests.get(
        "http://smarthome.webpython.graders.eldf.ru/api/user.controller",
        headers={"Authorization": "Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"}
    )
    controllers = json.loads(request.text)['data']
    data = {controller['name']: controller['value'] for controller in controllers}

    if bedroom_temperature and boiler_temperature is None:
        pass

    return data
