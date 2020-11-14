from django.shortcuts import render, redirect
from main.models import *
from datetime import date
import bcrypt
from django.contrib import messages
from time import strftime 

def index(request):
    return render(request, 'index.html')

def register(request):    
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        email = request.POST['email']
        try: 
            User.objects.get(email=email)
            messages.error(request, "A user with this email already exists!")
            return redirect('/')

        except: 
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()       

            new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
            )
            request.session['user_id'] = new_user.id
            return redirect("/success") 

def login(request):
    email = request.POST['email'] 
    logged_user = User.objects.filter(email = email)
    if logged_user:
        logged_user = logged_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/success')
        else:
            messages.error(request, "Incorrect password!")
            return redirect('/')
    else:
        messages.error(request, "No user exists with that email.")
        return redirect('/')

def success(request):
    if 'user_id' in request.session:

        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_trips': Trip.objects.exclude(planner = request.session['user_id']).exclude(guests = request.session['user_id']) 

        }
        return render(request, 'welcome.html', context)
    else:
        return redirect('/')

def new(request):
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'new.html', context)

def create(request):
    user = User.objects.get(id=request.session['user_id'])

    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')

    my_trip = Trip.objects.create(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        plan = request.POST['plan'],
        planner = user
    )

    return redirect('/submit')

def edit(request, trip_id):
    
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    new_start = trip.start_date.strftime('%Y-%m-%d')
    new_end = trip.end_date.strftime('%Y-%m-%d')

    context = {
        'trip': trip,
        'user': user,
        'new_start': new_start,
        'new_end': new_end,
    }

    return render(request, 'edit.html', context)

def update(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/{trip.id}/edit')

    trip_edit = Trip.objects.filter(id=trip_id).update(
        destination = request.POST['destination'],
        start_date = request.POST['start_date'],
        end_date = request.POST['end_date'],
        plan = request.POST['plan'],
        planner = user,
    )
    return redirect('/success')

def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/success')

def show_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['user_id'])

    context = {
        'trip': trip,
        'user': user,
    }
    return render(request, 'trip.html', context)

def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.going_with.add(trip)
    return redirect('/success')

def cancel(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.going_with.remove(trip)
    return redirect('/success')

def logout(request):
    request.session.clear()
    messages.error(request, "You have logged out.")
    return redirect('/')



# Create your views here.
