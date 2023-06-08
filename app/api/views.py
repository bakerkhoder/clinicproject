from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets
import requests
from ..models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


@api_view(['GET'])
def patientAppointment(request, pk):
    patient_id = Patient.objects.get(id=pk)
    appointment = Appointment.objects.filter(patient=patient_id)
    serialize = AppointmentSerializer(appointment, many=True)
    return Response(serialize.data)


@api_view(['GET'])
def nurseAppointment(request, pk):
    nurse_id = Nurse.objects.get(id=pk)
    appointment = Appointment.objects.filter(nurse=nurse_id)
    serialize = AppointmentSerializer(appointment, many=True)
    return Response(serialize.data)

@api_view(['GET'])
def DoctorAppointment(request, pk):
    doctor_id = Doctor.objects.get(id=pk)
    appointment = Appointment.objects.filter(doctor=doctor_id)
    serialize = AppointmentSerializer(appointment, many=True)
    return Response(serialize.data)



