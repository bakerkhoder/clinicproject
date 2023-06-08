from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Patient', PatientViewSet)
router.register(r'Doctor', DoctorViewSet)
router.register(r'Nurse', NurseViewSet)
router.register(r'Appointment', AppointmentViewSet)
router.register(r'User', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('patientAppointmentApi/<int:pk>', patientAppointment),
    path('nurseAppointmentApi/<int:pk>', nurseAppointment),
    path('doctorAppointmentApi/<int:pk>', DoctorAppointment),
]
