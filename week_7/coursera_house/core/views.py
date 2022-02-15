import json
import requests
from django.urls import reverse_lazy
from django.views.generic import FormView
from .models import Setting
from .form import ControllerForm

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
"""


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    @staticmethod
    def getting_the_status_of_all_controllers():
        request = requests.get(
            "http://smarthome.webpython.graders.eldf.ru/api/user.controller",
            headers={"Authorization": "Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"}
        )
        controllers = json.loads(request.text)['data']
        data = {controller['name']: controller['value'] for controller in controllers}
        return data

    @staticmethod
    def saving_the_status_of_controllers(data: list):
        request = requests.post(
            "http://smarthome.webpython.graders.eldf.ru/api/user.controller",
            headers={"Authorization": "Bearer 7920c5af9d3e65f13bb28873ed4d02c5896f941c8f2664020ccb217150254658"},
            data=json.dumps({"controllers": data})
        )
        return request.status_code

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
        bedroom_temperature = form.cleaned_data['bedroom_target_temperature']
        boiler_temperature = form.cleaned_data['hot_water_target_temperature']
        bedroom_light = form.cleaned_data['bedroom_light']
        bathroom_light = form.cleaned_data['bathroom_light']
        print(f'bedroom_temperature: {bedroom_temperature}')
        print(f'boiler_temperature: {boiler_temperature}')
        print(f'bedroom_light: {bedroom_light}')
        print(f'bathroom_light: {bathroom_light}')

        updated_values_1 = {'value': bedroom_temperature}
        controller_1, _ = Setting.objects.get_or_create(controller_name='bedroom_temperature',
                                                        label='Температура в спальне',
                                                        defaults=updated_values_1)
        controller_1.save()

        updated_values_2 = {'value': boiler_temperature}
        controller_2, _ = Setting.objects.get_or_create(controller_name='boiler_temperature',
                                                        label='Температура горячей воды бойлере',
                                                        defaults=updated_values_2)
        controller_2.save()

        data_that_requires_synchronization_with_controllers = [
            {"name": "bedroom_light", "value": bedroom_light},
            {"name": "bathroom_light", "value": bathroom_light}
        ]
        self.saving_the_status_of_controllers(data_that_requires_synchronization_with_controllers)

        return super(ControllerView, self).form_valid(form)


