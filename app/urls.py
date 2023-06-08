from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('about', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('doctor_register/', views.DoctorRegister, name='doctor_register'),
    path('nurse_register/', views.NurseRegister, name='nurse_register'),

    path('user_selection/', views.user_selection_post, name='user_selection'),

    path('Appointment/', views.AppointmentView, name='Appointment'),
    path('patient_appointment/<int:pk>', views.patientAppointment, name='patient_appointment'),
    path('nurse_appointment/<int:pk>', views.NurseAppointment, name='nurse_appointment'),
    path('Appointments/<int:pk>', views.AppointmentList, name='Appointments'),
    path('update_appointment/<int:pk>', views.UpdateAppointment, name='update_appointment'),
    path('delete_appointment/<int:pk>', views.DeleteAppointment, name='delete_appointment'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]
