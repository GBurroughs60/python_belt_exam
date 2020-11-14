from django.db import models
from datetime import date
from django import forms
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = "First Name needs to be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last Name needs to be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):   
            errors['email'] = "Invalid email address!"       
        if len(post_data['password']) < 7:
            errors['password'] = "Password needs to be at least 8 characters"
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = "Password and Confirm Password do not match. Please try again."        
        return errors

class TripManager(models.Manager):
    def trip_validator(self, post_data):
        errors = {}
        if len(post_data['destination']) < 2:
            errors['destination'] = "Destination needs to be at least 3 characters"
        if len(post_data['plan']) < 2:
            errors['plan'] = "Plan needs to be at least 3 characters"
        if post_data['start_date']:
            year,month,day = post_data['start_date'].split('-')
            if date(int(year),int(month),int(day)) <= date.today():
                errors['start_date'] = "Trip must be in the future!"
        if post_data['end_date']:
            year,month,day = post_data['end_date'].split('-')
            a,b,c = post_data['start_date'].split('-')
            if date(int(year),int(month),int(day)) <= date(int(a),int(b),int(c)):
                errors['end_date'] = "Trip end date can't be before Trip start date!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20, default = "password")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=40)
    planner = models.ForeignKey(User, related_name="planned_by", on_delete = models.CASCADE)
    guests = models.ManyToManyField(User, related_name="going_with")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

# Create your models here.