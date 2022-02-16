import json
import requests
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Setting
from .form import ControllerForm
from ..settings import SMART_HOME_API_URL, SMART_HOME_ACCESS_TOKEN

"""
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
method of getting the current user

request = requests.get("http://smarthome.webpython.graders.eldf.ru/api/auth.current", headers={"Authorization": 
"Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"})
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
method for getting the state of all controllers

request = requests.get("http://smarthome.webpython.graders.eldf.ru/api/user.controller", headers={"Authorization": 
"Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"})
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
method for saving the state of controllers

request = requests.post(
    "http://smarthome.webpython.graders.eldf.ru/api/user.controller",
    headers={"Authorization": "Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"},
    data=json.dumps({"controllers": [{"name": "air_conditioner", "value": False}, {"name": "bedroom_light", "value": 
    False}]})
)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
celery -A coursera_house.celery:app worker --pool=solo -l info - launching worker
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
celery -A coursera_house.celery:app beat -l info launching task every 5 minutes
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
celery -A coursera_house.celery:app flower --port=5555
celery -A coursera_house.celery flower
"""


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    @staticmethod
    def getting_the_status_of_all_controllers():
        request = requests.get(SMART_HOME_API_URL, headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN})
        controllers = json.loads(request.text)['data']
        data = {controller['name']: controller['value'] for controller in controllers}
        return data

    @staticmethod
    def saving_the_status_of_controllers(data: list):
        print(True)
        print(SMART_HOME_API_URL, type(SMART_HOME_API_URL))
        print(SMART_HOME_ACCESS_TOKEN, type(SMART_HOME_ACCESS_TOKEN))
        print(f'data from saving_the_status_of_controllers: {data}')
        request = requests.post(SMART_HOME_API_URL, headers={"Authorization": "Bearer " + SMART_HOME_ACCESS_TOKEN},
                                data=json.dumps({"controllers": data}))
        return request.text

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        context['data'] = self.getting_the_status_of_all_controllers()
        print(self.getting_the_status_of_all_controllers())
        return context

    def get_initial(self):
        """Returns the initial data to use for forms on this view"""

        data = self.getting_the_status_of_all_controllers()

        initial = super().get_initial()
        initial['bedroom_light'] = data['bedroom_light']
        initial['bathroom_light'] = data['bathroom_light']

        return initial

    def form_valid(self, form):
        print(form.cleaned_data)
        bedroom_temperature = form.cleaned_data['bedroom_target_temperature']
        boiler_temperature = form.cleaned_data['hot_water_target_temperature']
        bedroom_light = form.cleaned_data['bedroom_light']
        bathroom_light = form.cleaned_data['bathroom_light']
        print(f'bedroom_temperature: {bedroom_temperature}')
        print(f'boiler_temperature: {boiler_temperature}')
        print(f'bedroom_light: {bedroom_light}')
        print(f'bathroom_light: {bathroom_light}')

        updated_values_1 = {'value': bedroom_temperature}
        controller_1, _ = Setting.objects.update_or_create(controller_name='bedroom_temperature',
                                                           label='Желаемая температура в спальне',
                                                           defaults=updated_values_1)
        print(f'controller_1: {controller_1}\ncontroller_1.value: {controller_1.value}')
        controller_1.save()

        updated_values_2 = {'value': boiler_temperature}
        controller_2, _ = Setting.objects.update_or_create(controller_name='boiler_temperature',
                                                           label='Желаемая температура горячей воды',
                                                           defaults=updated_values_2)
        print(f'controller_2: {controller_2}\ncontroller_2.value: {controller_2.value}')
        controller_2.save()

        data_that_requires_synchronization_with_controllers = [
            {"name": "bedroom_light", "value": bedroom_light},
            {"name": "bathroom_light", "value": bathroom_light},
            {"name": "bedroom_temperature", "value": bedroom_temperature},
            {"name": "boiler_temperature", "value": boiler_temperature}
        ]
        self.saving_the_status_of_controllers(data_that_requires_synchronization_with_controllers)


        # data_that_requires_synchronization_with_controllers1 = [
        #     {"name": "bedroom_temperature", "value": bedroom_temperature},
        #     {"name": "boiler_temperature", "value": boiler_temperature}
        # ]
        # self.saving_the_status_of_controllers(data_that_requires_synchronization_with_controllers1)

        return super(ControllerView, self).form_valid(form)


