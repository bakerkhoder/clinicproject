from django import forms
from django.forms import ModelForm
from .models import Appointment


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        exclude = ['doctor']
        widgets = {
            'appoint_date': forms.DateInput(attrs={'type': 'date'}),
            'appoint_time': forms.TimeInput(attrs={'type': 'time'}),
        }
