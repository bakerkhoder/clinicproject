from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import *
from .forms import AppointmentForm
import requests
import json
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_email = request.POST['username_email'].lower()
        password = request.POST['password']

        response = requests.get('http://127.0.0.1:8000/api/User/')
        users = response.json()

        user = None
        for user_data in users:
            if (user_data['username'] == username_email or user_data['email'] == username_email) and check_password(password, user_data['password']):
                user = User.objects.get(username=user_data['username'])
                login(request, user)
                return redirect('home')

        messages.error(request, 'Username/email or password is incorrect')

    return render(request, 'app/login.html')


def logoutUser(request):
    logout(request)
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, format_html('Dear {}, please go to your email {} inbox and click on \
                the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.',
                                              user, to_email))
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def register(request):

    if request.method == 'POST':

        name = request.POST['name']
        dob = request.POST['dob']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        data = {
            'name': name,
            'dob': dob,
            'address': address,
            'phone': phone,
            'email': email,
            'username': username,
            'password': password,
            'password_confirm': confirm_password
        }

        response = requests.post('http://127.0.0.1:8000/api/Patient/', json=data)

        if response.status_code == 201:
            patient_id = response.json()['id']
            patient = Patient.objects.get(id=patient_id)
            user = patient.username
            activateEmail(request, user, email)
            messages.success(request, 'Patient created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Patient creation failed')

    return render(request, 'app/patient_register.html')


def DoctorRegister(request):

    if request.method == 'POST':

        name = request.POST['name']
        specialty = request.POST['specialty']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        data = {
            'name': name,
            'specialty': specialty,
            'email': email,
            'phone': phone,
            'username': username,
            'password': password,
            'password_confirm': confirm_password
        }

        response = requests.post('http://127.0.0.1:8000/api/Doctor/', json=data)
        if response.status_code == 201:
            doctor_id = response.json()['id']
            doctor = Doctor.objects.get(id=doctor_id)
            user = doctor.username
            activateEmail(request, user, email)
            messages.success(request, 'Doctor created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Doctor creation failed')
    return render(request, 'app/doctor_register.html')


def NurseRegister(request):

    if request.method == 'POST':

        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        data = {
            'username': username,
            'password': password,
            'password_confirm': confirm_password,
            'email': email,
            'name': name,
            'phone': phone,
        }

        response = requests.post('http://127.0.0.1:8000/api/Nurse/', json=data)
        if response.status_code == 201:
            nurse_id = response.json()['id']
            nurse = Nurse.objects.get(id=nurse_id)
            user = nurse.username
            activateEmail(request, user, email)
            messages.success(request, 'Nurse created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Nurse creation failed')
    return render(request, 'app/nurse_register.html')


def user_selection_post(request):
    if request.method == 'POST':
        user_type = request.POST.get('post')
        if user_type == 'Patient':
            return render(request, 'app/patient_register.html')
        elif user_type == 'Doctor':
            return render(request, 'app/doctor_register.html')
        else:
            return render(request, 'app/nurse_register.html')
    return render(request, 'app/user_selection_post.html')


def home(request):
    return render(request, 'app/home.html')


@login_required(login_url='login')
def AppointmentView(request):

    if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
        return HttpResponseForbidden('You are not allowed here.')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment_data = {
                'appoint_date': form.cleaned_data['appoint_date'].strftime('%Y-%m-%d'),
                'appoint_time': form.cleaned_data['appoint_time'].strftime('%H:%M:%S'),
                'treatment': form.cleaned_data['treatment'],
                'patient': form.cleaned_data['patient'].id,
                'doctor': request.user.doctor.id,
                'nurse': form.cleaned_data['nurse'].id
            }

            response = requests.post('http://127.0.0.1:8000/api/Appointment/', data=json.dumps(appointment_data), headers={'Content-Type': 'application/json'})
            if response.status_code == 201:
                return redirect('Appointment')
            else:
                form.add_error(None, 'Error occurred while saving the data.')
    else:
        form = AppointmentForm()
    context = {'form': form}
    return render(request, 'app/Appointment.html', context)


@login_required(login_url='login')
def AppointmentList(request, pk):

    if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
        return HttpResponseForbidden('You are not allowed here.')

    response = requests.get(f'http://127.0.0.1:8000/api/doctorAppointmentApi/{pk}')
    response1 = requests.get(f'http://127.0.0.1:8000/api/Doctor/{pk}')
    doctor1 = response1.json()
    appointments = response.json()
    for appointment in appointments:
        appointment['patient'] = Patient.objects.get(id=appointment['patient']).name
        appointment['doctor'] = doctor1['name']
        appointment['nurse'] = Nurse.objects.get(id=appointment['nurse']).name
    return render(request, 'app/Appointments.html', {'appointments': appointments})


@login_required(login_url='login')
def DeleteAppointment(request, pk):

    if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
        return HttpResponseForbidden('You are not allowed here.')

    if request.method == 'POST':
        response = requests.delete(f'http://127.0.0.1:8000/api/Appointment/{pk}/')
        return redirect('Appointments', pk=request.user.doctor.id)
    return render(request, 'app/delete_appointment.html')


@login_required(login_url='login')
def UpdateAppointment(request, pk):

    if not request.user.is_authenticated or not hasattr(request.user, 'doctor'):
        return HttpResponseForbidden('You are not allowed here.')

    if not request.user.doctor:
        return HttpResponse('You are not Allowd here')

    apointment = Appointment.objects.get(id=pk)
    form = AppointmentForm(instance=apointment)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=apointment)
        appoint_date = request.POST.get('appoint_date')
        appoint_time = request.POST.get('appoint_time')
        treatment = request.POST.get('treatment')
        patient_id = request.POST.get('patient')
        nurse_id = request.POST.get('nurse')

        appointment_data = {
            'appoint_date': appoint_date,
            'appoint_time': appoint_time,
            'treatment': treatment,
            'patient': patient_id,
            'doctor': request.user.doctor.id,
            'nurse': nurse_id
        }
        response = requests.put(f'http://127.0.0.1:8000/api/Appointment/{pk}/', data=json.dumps(appointment_data), headers={'Content-Type': 'application/json'})
        return redirect('Appointments', pk=request.user.doctor.id)

        if response.status_code == 201:
            return redirect('Appointments', pk=request.user.doctor.id)
        else:
            form.add_error(None, 'Error occurred while updating the data.')
    else:
        form = AppointmentForm(instance=apointment)

    context = {'form': form}
    return render(request, 'app/update_appointment.html', context)


@login_required(login_url='login')
def patientAppointment(request, pk):

    if not request.user.is_authenticated or not hasattr(request.user, 'patient'):
        return HttpResponseForbidden('You are not allowed here.')

    # patient_id = Patient.objects.get(id=pk)
    # appointments = Appointment.objects.filter(patient=patient_id)
    response = requests.get(f'http://127.0.0.1:8000/api/patientAppointmentApi/{pk}')
    response1 = requests.get(f'http://127.0.0.1:8000/api/Patient/{pk}')
    patient1 = response1.json()
    appointments = response.json()
    for appointment in appointments:
        doctor_id = appointment['doctor']
        doctor1 = requests.get(f'http://127.0.0.1:8000/api/Doctor/{doctor_id}')
        doctor_name = doctor1.json()['name']
        nurse_id = appointment['nurse']
        nurse1 = requests.get(f'http://127.0.0.1:8000/api/Nurse/{nurse_id}')
        nurse_name = nurse1.json()['name']
        appointment['patient'] = patient1['name']
        appointment['doctor'] = doctor_name
        appointment['nurse'] = nurse_name
    context = {'appointments': appointments}
    return render(request, 'app/user_appointment.html', context)


@login_required(login_url='login')
def NurseAppointment(request, pk):

    if not request.user.is_authenticated or not hasattr(request.user, 'nurse'):
        return HttpResponseForbidden('You are not allowed here.')

    response = requests.get(f'http://127.0.0.1:8000/api/nurseAppointmentApi/{pk}')
    response1 = requests.get(f'http://127.0.0.1:8000/api/Nurse/{pk}')
    nurse1 = response1.json()
    appointments = response.json()
    for appointment in appointments:
        patient_id = appointment['patient']
        patient1 = requests.get(f'http://127.0.0.1:8000/api/Patient/{patient_id}')
        patient_name = patient1.json()['name']
        doctor_id = appointment['doctor']
        doctor1 = requests.get(f'http://127.0.0.1:8000/api/Doctor/{doctor_id}')
        doctor_name = doctor1.json()['name']
        appointment['patient'] = patient_name
        appointment['doctor'] = doctor_name
        appointment['nurse'] = nurse1['name']
    context = {'appointments': appointments}
    return render(request, 'app/nurse_appointment.html', context)


def about(request):
    return render(request, 'app/about.html')
