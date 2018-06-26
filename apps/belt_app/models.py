# Inside your app's models.py file
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        errors = []
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-z]+$')
        if len(postData['first_name']) < 2:
            errors.append("First name is too short!")
        elif not NAME_REGEX.match(postData['first_name']):
            errors.append("First name can be letters only!")
        if len(postData['last_name']) < 2:
            errors.append("Last name is too short!")
        elif not NAME_REGEX.match(postData['last_name']):
            errors.append("Last name can be letters only!")
        if len(postData['email']) < 1:
            errors.append("Email is too short!")
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append("Invalid email address!")
        elif User.objects.filter(email=postData['email']).exists():
            errors.append("Email already exists!")
        if len(postData['password']) < 8:
            errors.append("Password has to be at least 8 characters in length!")
        if postData['password'] != postData['confirm_password']:
            errors.append("Passwords don't match!")
        if len(errors):
            return errors
        else:
            me = User.objects.create(
                first_name = postData['first_name'],
                last_name = postData['last_name'],
                email = postData['email'],
                password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            )
            return me

    def validateLogin(self, postData):
        existing_user_list = User.objects.filter(email=postData['email'])
        if len(existing_user_list):
            if bcrypt.checkpw(postData['password'].encode(), existing_user_list[0].password.encode()):
                return existing_user_list[0]
        return 'invalid email / password combination'
    
    # def validateEdit(self,postData):
    #     errors = []
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    #     NAME_REGEX = re.compile(r'^[a-zA-z]+$')
    #     if len(postData['first_name']) < 2:
    #         errors.append("First name is too short!")
    #     if not NAME_REGEX.match(postData['first_name']):
    #         errors.append("First name can be letters only!")
    #     if len(postData['last_name']) < 2:
    #         errors.append("Last name is too short!")
    #     if not NAME_REGEX.match(postData['last_name']):
    #         errors.append("Last name can be letters only!")
    #     if len(postData['email']) < 1:
    #         errors.append("Email is too short!")
    #     elif not EMAIL_REGEX.match(postData['email']):
    #         errors.append("Invalid email address!")
    #     # if User.objects.get(email=postData['email']).exists():
    #     #     errors.append("Email already exists!")
    #     if len(errors):
    #         return errors
    #     else:
    #         user = User.objects.get(id=postData['hidden_id'])
    #         user.first_name = postData['first_name']
    #         user.last_name = postData['last_name']
    #         user.email = postData['email']
    #         user.save()
    #         return user

class TripManager(models.Manager):
    def validateTrip(self, postData):
        errors = []
        if postData['startdate'] == "":
            errors.append("Starting date cannot be empty!")
        if postData['enddate'] == "":
            errors.append("Ending date cannot be empty!")
        if len(errors):
            return errors
        else: 
            startDt = datetime.strptime(postData['startdate'], '%Y-%m-%d').date()
            endDt = datetime.strptime(postData['enddate'], '%Y-%m-%d').date()
            today = date.today()
            if len(postData['destination']) < 1:
                errors.append("Destination cannot be empty!")
            if len(postData['description']) < 1:
                errors.append("Description cannot be empty!")
            if startDt < today:
                errors.append("Starting date should be future-dated!")
            if endDt < today:
                errors.append("Ending date should be future-dated!")
            if startDt > endDt:
                errors.append("Starting date should not be before the ending date!")
            if len(errors):
                return errors
            else:
                me = Trip.objects.create(
                    destination = postData['destination'],
                    description = postData['description'],
                    startDate = startDt,
                    endDate = endDt,
                # planner = User.objects.get(id=)
                # poster = User.objects.get(id=user_id)
                )
                return me
            # return newquote

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return "<User object: name:{} {}, email:{}, created at: {}>".format(self.first_name, self.last_name, self.email, self.created_at)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    # like = models.IntegerField(default=0,blank=True, null=True)
    joined_users = models.ManyToManyField(User, related_name="joined_trips")
    # planner = models.IntegerField(default=None,blank=True, null=True)
    planner = models.ForeignKey(User, related_name = "planned_trips", blank=True, null=True)
    objects = TripManager()
    # def __repr__(self):
    #     return "<Quote object: author:{}, quote:{}, author_id:{}>".format(self.author, self.quote, self.Author_id)
