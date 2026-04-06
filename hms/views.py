from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment, Doctor
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AppointmentSerializer

def view_home(request):
    doctors = Doctor.objects.all()
    return render(request, 'hms/home.html', {'doctors': doctors})


def view_about(request):
    return render(request,'hms/about.html')


def view_services(request):
    return render(request,'hms/services.html')


def view_departments(request):
    return render(request,'hms/departments.html')


def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request,'hms/doctors.html', {'doctors': doctors})


def view_appointments(request):
    data = Appointment.objects.all()
    return render(request, 'hms/appointments.html', {'data': data})


def add_appointment(request):
    doctors = Doctor.objects.all()

    if request.method == "POST":
        patient = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')

        if not doctor_id:
            return render(request, 'hms/home.html', {
                'doctors': doctors,
                'error': 'Please select doctor ❌'
            })

        doctor = Doctor.objects.get(id=doctor_id)

        # check availability
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            return render(request, 'hms/home.html', {
                'doctors': doctors,
                'error': 'Doctor not available ❌'
            })

        # SAVE
        Appointment.objects.create(
            patient_name=patient,
            doctor=doctor,
            date=date,
            time=time,
            message=message
        )

        return redirect('appointments')   # 🔥 MAIN FIX

    return redirect('home')


def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    doctors = Doctor.objects.all()

    if request.method == "POST":
        appointment.patient_name = request.POST.get('patient')
        appointment.doctor = Doctor.objects.get(id=request.POST.get('doctor'))
        appointment.date = request.POST.get('date')
        appointment.time = request.POST.get('time')
        appointment.message = request.POST.get('message')
        appointment.save()
        return redirect('appointments')

    return render(request, 'hms/edit_appointment.html', {
        'appointment': appointment,
        'doctors': doctors
    })


def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('appointments')

@api_view(['GET'])
def api_appointments(request):
    data = Appointment.objects.all()
    serializer = AppointmentSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_add_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'})
    return Response(serializer.errors)