from __future__ import unicode_literals
import re
import bcrypt

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def registration_validation(self, data):
        errors = []
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        alpha_only = re.compile(r'^[a-zA-Z -]+$')
        password_length = re.compile(r'^([a-zA-Z0-9@*#]{8,15})$')
        for fieldname, value in data.items():
            if len(value) < 1:
                errors.append(fieldname + " cannot be empty!")
        if re.match(alpha_only, data['first_name']) is None:
            errors.append("First Name must be letters only!")
        if re.match(alpha_only, data['last_name']) is None:
            errors.append("Last Name must be letters only!")
        if re.match(email_regex, data['email']) is None:
            errors.append("Invalid E-Mail format!")
        if data['password'] != data['confirm_password']:
            errors.append("Passwords must match!")
        if self.filter(email=data['email']).count() > 0:
            errors.append("E-Mail already registered!")
        if re.match(password_length, data['password']) is None:
            errors.append("Password must be Letters, Numbers, Special Characacters(@ * #) and 8-15 characters long!")
        return errors
    def login_validation(self, data):
        errors = []
        for fieldname, value in data.items():
            if len(value) < 1:
                errors.append(fieldname + " cannot be empty!")
        if len(errors):
            return errors
        if self.filter(email=data['email']).count() < 1:
            errors.append("E-Mail not registered!")
        else:
            trying = self.filter(email=data['email'])
            if not bcrypt.checkpw(data['password'].encode(), trying[0].password.encode()):
                errors.append("Password not correct!")
        return errors
        


class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.first_name + self.last_name

    