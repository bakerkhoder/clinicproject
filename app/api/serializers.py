from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return user


class PasswordConfirmationSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("The passwords do not match.")
        return data


class PatientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    dob = serializers.DateField()
    address = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(max_length=128, write_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateField(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")

        email = validated_data.pop('email')

        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        validated_data['username'] = user
        patient = Patient.objects.create(**validated_data, email=email)

        return patient


class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    specialty = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(max_length=128, write_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateField(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match")

        email = validated_data.pop('email')
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        validated_data['username'] = user
        doctor = Doctor.objects.create(**validated_data, email=email)
        return doctor


class NurseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    password_confirm = serializers.CharField(max_length=128, write_only=True)
    email = serializers.EmailField(write_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateField(read_only=True)

    class Meta:
        model = Nurse
        fields = '__all__'
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirm = validated_data.pop('password_confirm')
        email = validated_data.pop('email')
        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")
        username = validated_data.pop('username')
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        validated_data['username'] = user
        nurse = Nurse.objects.create(**validated_data)
        return nurse


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'

# class AppointmentSerializer(serializers.ModelSerializer):
#     patient = PatientSerializer()
#     doctor = DoctorSerializer()
#     nurse = NurseSerializer()
#
#     class Meta:
#         model = Appointment
#         fields = '__all__'
#
#     def create(self, validated_data):
#         patient_data = validated_data.pop('patient')
#         doctor_data = validated_data.pop('doctor')
#         nurse_data = validated_data.pop('nurse')
#         patient = Patient.objects.create(**patient_data)
#         doctor = Doctor.objects.create(**doctor_data)
#         nurse = Nurse.objects.create(**nurse_data)
#         appointment = Appointment.objects.create(patient=patient, doctor=doctor, nurse=nurse, **validated_data)
#         return appointment
#
#     def update(self, instance, validated_data):
#         instance.appoint_date = validated_data.get('validated_data', instance.appoint_date)
#         instance.appoint_time = validated_data.get('appoint_time', instance.appoint_time)
#         instance.treatment = validated_data.get('treatment', instance.treatment)
#
#         patient_data = validated_data.pop('patient', None)
#
#         if patient_data:
#             patient_serializer = PatientSerializer(instance.patient, data=patient_data)
#             patient_serializer.is_valid(raise_exception=True)
#             patient_serializer.save()
#
#         doctor_data = validated_data.pop('doctor', None)
#
#         if doctor_data:
#             doctor_serializer = DoctorSerializer(instance.doctor, data=doctor_data)
#             doctor_serializer.is_valid(raise_exception=True)
#             doctor_serializer.save()
#
#         nurse_data = validated_data.pop('nurse', None)
#
#         if patient_data:
#             nurse_serializer = NurseSerializer(instance.nurse, data=nurse_data)
#             nurse_serializer.is_valid(raise_exception=True)
#             nurse_serializer.save()
#
#         # save appointment instance
#         instance.save()
#         return instance
