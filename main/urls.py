from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('trips/new', views.new),
    path('trips/<int:trip_id>/delete', views.delete),
    path('create', views.create),
    path('submit', views.success),
    path('trips/<int:trip_id>', views.show_trip),
    path('trips/<int:trip_id>/edit', views.edit),
    path('trips/<int:trip_id>/update', views.update),
    path('trips/<int:trip_id>/join', views.join),
    path('trips/<int:trip_id>/cancel', views.cancel),
    path('logout', views.logout),
]