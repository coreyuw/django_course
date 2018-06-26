from django.shortcuts import render, HttpResponse, redirect
from .models import User, Trip
from django.contrib import messages
from datetime import datetime
from django.urls import reverse

def index(request):
    return render(request, 'belt_app/index.html')

def createUser(request):
    result = User.objects.validateRegistration(request.POST)
    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
    return redirect('/dashboard')

def login(request):
    result = User.objects.validateLogin(request.POST)
    if type(result) is str:
        messages.error(request, result)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/dashboard')

def dashboard(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'my_trips': Trip.objects.filter(joined_users= User.objects.get(id=request.session['user_id'])),
        'other_trips': Trip.objects.all().exclude(joined_users= User.objects.get(id=request.session['user_id']))
    }
    return render(request, 'belt_app/dashboard.html', context)

def logout(request):
    request.session['user_id'] = 0
    return redirect('/')

def addtrip(request):
    context={
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'belt_app/add_trip.html', context)

def update(request):
    result = Trip.objects.validateTrip(request.POST)
    # user = User.objects.get(id=request.POST['hidden_id'])
    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect("/addtrip")
    else:
        this_planner = User.objects.get(id=request.session['user_id'])
        this_planner.planned_trips.add(result)
        this_planner.joined_trips.add(result)
        return redirect("/dashboard")

def view(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'planner': User.objects.get(planned_trips = Trip.objects.get(id = trip_id)),
        'other_users': User.objects.filter(joined_trips=Trip.objects.get(id=trip_id)).exclude(planned_trips = Trip.objects.get(id = trip_id))
    }
    return render(request, 'belt_app/view.html', context)


def cancel(request, trip_id):
    this_traveller = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=trip_id)
    this_traveller.joined_trips.remove(this_trip)
    return redirect("/dashboard")

def delete(request, trip_id):
    this_delete = Trip.objects.get(id=trip_id)
    this_delete.delete()
    return redirect('/dashboard')

def join(request, trip_id):
    this_traveller = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=trip_id)
    this_traveller.joined_trips.add(this_trip)
    return redirect('/dashboard')

# def add(request):
#     result = Trip.objects.validateTrip(request.POST, request.session['user_id'])
#     if type(result) is list:
#         for error in result:
#             messages.error(request, error)
#         return redirect("/dashboard")
#     else:
#         this_author = User.objects.get(id=request.session['user_id'])
#         this_author.posted_quotes.add(result)
#         return redirect('/dashboard')

# def show(request, user_id):
#     context = {
#         'quotes': Quote.objects.filter(poster=User.objects.get(id=user_id)),
#         'user': User.objects.get(id=user_id)
#     }
#     return render(request, 'quote_dash_app/show.html', context)

# def like(request, quote_id):
#     quote = Quote.objects.get(id=quote_id)
#     me = User.objects.get(id=request.session['user.id'])
#     quote.liked_users.add(me)
#     quote.save()
#     return redirect('/quotes')

# def delete(request, quote_id):
#     this_delete = Quote.objects.get(id=quote_id)
#     this_delete.delete()
#     return redirect('/quotes')

