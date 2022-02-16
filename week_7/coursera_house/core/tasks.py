from __future__ import absolute_import, unicode_literals
import json
import requests
from celery import task
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from .models import Setting
from ..settings import SMART_HOME_ACCESS_TOKEN, SMART_HOME_API_URL, EMAIL_RECEPIENT, EMAIL_HOST_USER


@task()
def smart_home_manager():

    request = requests.get(
        SMART_HOME_API_URL, headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN}
    )
    controllers = json.loads(request.text)['data']
    data = {controller['name']: controller['value'] for controller in controllers}

    """Если есть протечка воды (leak_detector=true), закрыть холодную (cold_water=false) и горячую (hot_water=false) 
    воду и отослать письмо в момент обнаружения."""

    if data['leak_detector']:
        data_that_requires_to_change_in_controllers = [
            {"name": "cold_water", "value": False},
            {"name": "hot_water", "value": False}
        ]
        request = requests.post(SMART_HOME_API_URL,
                                headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                data=json.dumps({"controllers": data_that_requires_to_change_in_controllers}))
        print(request.status_code)

        send_mail(
            'Water leak',
            'There is a water leak. We had to close the cold and hot water at the time of detection',
            EMAIL_HOST_USER,
            [EMAIL_RECEPIENT],
            fail_silently=False,
        )

    """Если холодная вода (cold_water) закрыта, немедленно выключить бойлер (boiler) и стиральную машину 
    (washing_machine) и ни при каких условиях не включать их, пока холодная вода не будет снова открыта"""

    if not data['cold_water']:
        data_that_requires_to_change_in_controllers = [
            {"name": "boiler", "value": False},
            {"name": "washing_machine", "value": 'off'}
        ]
        request = requests.post(SMART_HOME_API_URL,
                                headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                data=json.dumps({"controllers": data_that_requires_to_change_in_controllers}))
        print(request.status_code)

        send_mail(
            'Cold water is closed',
            """Since the cold water is closed, we had to turn off the boiler and washing machine at the time of 
detection""",
            EMAIL_HOST_USER,
            [EMAIL_RECEPIENT],
            fail_silently=False,
        )

    """Если горячая вода имеет температуру (boiler_temperature) меньше чем hot_water_target_temperature - 10%, нужно 
    включить бойлер (boiler), и ждать пока она не достигнет температуры hot_water_target_temperature + 10%, после чего 
    в целях экономии энергии бойлер нужно отключить"""

    boiler_temperature_from_api = data['boiler_temperature']
    print(f'boiler_temperature_from_api: {boiler_temperature_from_api}')

    try:
        boiler_temperature_from_db = Setting.objects.get(controller_name='boiler_temperature').value
    except ObjectDoesNotExist:
        boiler_temperature_from_db = None
    print(f'boiler_temperature_from_db: {boiler_temperature_from_db}')

    if boiler_temperature_from_db is not None:
        if boiler_temperature_from_api is not None:
            if boiler_temperature_from_api < boiler_temperature_from_db * 0.9:

                request = requests.post(SMART_HOME_API_URL,
                                        headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                        data=json.dumps({"controllers": {"name": "boiler", "value": True}}))
                print(request.status_code)

            if data['boiler_temperature'] >= boiler_temperature_from_db * 1.1:

                request = requests.post(SMART_HOME_API_URL,
                                        headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                        data=json.dumps({"controllers": {"name": "boiler", "value": False}}))
                print(request.status_code)
        else:
            data_that_requires_to_change_in_controllers = [
                {"name": "cold_water", "value": True},
                {"name": "boiler", "value": True}
            ]
            request = requests.post(SMART_HOME_API_URL,
                                    headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": data_that_requires_to_change_in_controllers}))
            print(request.status_code)

    """Если шторы частично открыты (curtains == “slightly_open”), то они находятся на ручном управлении - это значит
     их состояние нельзя изменять автоматически ни при каких условиях.

    Если на улице (outdoor_light) темнее 50, открыть шторы (curtains), но только если не горит лампа в спальне 
    (bedroom_light). Если на улице (outdoor_light) светлее 50, или горит свет в спальне (bedroom_light), закрыть 
    шторы. Кроме случаев когда они на ручном управлении"""

    if data['curtains'] != 'slightly_open':

        if data['outdoor_light'] < 50 and not data['bedroom_light']:
            request = requests.post(SMART_HOME_API_URL,
                                    headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": {"name": "curtains", "value": 'open'}}))
            print(request.status_code)

        elif data['outdoor_light'] > 50 or data['bedroom_light']:
            request = requests.post(SMART_HOME_API_URL,
                                    headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": {"name": "curtains", "value": 'close'}}))
            print(request.status_code)

        """Если обнаружен дым (smoke_detector), немедленно выключить следующие приборы [air_conditioner, bedroom_light, 
        bathroom_light, boiler, washing_machine], и ни при каких условиях не включать их, пока дым не исчезнет."""

    if data['smoke_detector']:
        data_that_requires_to_change_in_controllers = [
            {"name": "air_conditioner", "value": False},
            {"name": "bedroom_light", "value": False},
            {"name": "bathroom_light", "value": False},
            {"name": "boiler", "value": False},
            {"name": "washing_machine", "value": 'off'}
        ]
        request = requests.post(SMART_HOME_API_URL,
                                headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                data=json.dumps({"controllers": data_that_requires_to_change_in_controllers}))
        print(request.status_code)

    """Если температура в спальне (bedroom_temperature) поднялась выше bedroom_target_temperature + 10% - включить 
    кондиционер (air_conditioner), и ждать пока температура не опустится ниже bedroom_target_temperature - 10%, 
    после чего кондиционер отключить."""

    bedroom_temperature_from_api = data['bedroom_temperature']
    print(f'bedroom_temperature_from_api: {bedroom_temperature_from_api}')

    try:
        bedroom_temperature_from_db = Setting.objects.get(controller_name='bedroom_temperature').value

    except ObjectDoesNotExist:
        bedroom_temperature_from_db = None
    print(f'bedroom_temperature_from_db: {bedroom_temperature_from_db}')

    if bedroom_temperature_from_db is not None:
        # if bedroom_temperature_from_api is not None:
        if bedroom_temperature_from_api >= boiler_temperature_from_db * 1.1:

            request = requests.post(SMART_HOME_API_URL,
                                    headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": {"name": "air_conditioner", "value": True}}))
            print(request.status_code)

        if bedroom_temperature_from_api <= boiler_temperature_from_db * 0.9:

            request = requests.post(SMART_HOME_API_URL,
                                    headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                    data=json.dumps({"controllers": {"name": "air_conditioner", "value": False}}))
            print(request.status_code)
