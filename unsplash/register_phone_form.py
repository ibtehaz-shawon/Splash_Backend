from django.forms import forms, ModelForm

import unsplash
from unsplash.models import DeviceData


class RegisterForm(ModelForm):

    class Meta:
        model = DeviceData
        fields = ('device_id', 'device_height', 'device_width')