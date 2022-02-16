from __future__ import absolute_import, unicode_literals
import json
import os

import requests
from celery import task
from django.core.exceptions import ObjectDoesNotExist
from .models import Setting
from ..settings import SMART_HOME_ACCESS_TOKEN, SMART_HOME_API_URL


@task()
def smart_home_manager():

    try:
        bedroom_temperature_from_data_base = Setting.objects.get(controller_name='bedroom_temperature')
        value_of_bedroom_temperature_from_data_base = bedroom_temperature_from_data_base.value
    except ObjectDoesNotExist:
        value_of_bedroom_temperature_from_data_base = None

    try:
        boiler_temperature_from_data_base = Setting.objects.get(controller_name='boiler_temperature')
        value_of_boiler_temperature_from_data_base = boiler_temperature_from_data_base.value
    except ObjectDoesNotExist:
        value_of_boiler_temperature_from_data_base = None
    print(f'value_of_bedroom_temperature_from_data_base: {value_of_bedroom_temperature_from_data_base}, '
          f'{type(value_of_bedroom_temperature_from_data_base)}')
    print(f'value_of_boiler_temperature_from_data_base: {value_of_boiler_temperature_from_data_base}, '
          f'{type(value_of_boiler_temperature_from_data_base)}')
    request = requests.get(
        SMART_HOME_API_URL, headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN}
    )
    controllers = json.loads(request.text)['data']
    data = {controller['name']: controller['value'] for controller in controllers}

    value_of_bedroom_temperature_from_api = data['bedroom_temperature']
    value_of_boiler_temperature_from_api = data['boiler_temperature']
    print(f'value_of_bedroom_temperature_from_api: {value_of_bedroom_temperature_from_api}, '
          f'{type(value_of_bedroom_temperature_from_api)}')

    print(f'value_of_boiler_temperature_from_api: {value_of_boiler_temperature_from_api}, '
          f'{type(value_of_boiler_temperature_from_api)}')

    if value_of_bedroom_temperature_from_data_base and value_of_boiler_temperature_from_data_base is None:
        pass
    else:
        if value_of_bedroom_temperature_from_data_base == value_of_bedroom_temperature_from_api and \
           value_of_boiler_temperature_from_data_base == value_of_boiler_temperature_from_api:
            pass
        else:
            data_that_requires_synchronization_with_controllers = [
                {"name": "bedroom_temperature", "value": value_of_bedroom_temperature_from_data_base},
                {"name": "boiler_temperature", "value": value_of_boiler_temperature_from_data_base}
            ]

            request = requests.post(SMART_HOME_API_URL, headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": data_that_requires_synchronization_with_controllers}
                                                    ))
            return request.status_code, json.loads(request.text)['field_problems']


