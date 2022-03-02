from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Flight, Passenger
# Create your views here.


def index(request):
  return render(request, "flights/index.html", {
    "flights": Flight.objects.all()
  })

def flight(request, flight_id):
  try:
    flight = Flight.objects.get(pk=flight_id)
  except Exception:
    raise Http404("No such flight!")
  return render(request, "flights/flight.html", {
    "flight": flight,
    "passengers": flight.passengers.all(), # all passengers
    "non_passengers": Passenger.objects.exclude(flights=flight).all() # Passengers not on the flight

  })


def book(request, flight_id):
  if request.method == "POST":
    flight = Flight.objects.get(pk=flight_id)
    passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
    passenger.flights.add(flight)

    return HttpResponseRedirect(reverse("flights:flight", args=(flight_id, )))
