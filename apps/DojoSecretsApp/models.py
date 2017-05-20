# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, postData):
        print "***REGISTRATION ATTEMPTED***"
        errors = []
        if len(postData['first_name']) < 1:
            errors.append('First name cannot be blank.')
        if len(postData['first_name']) <3:
            errors.append('First name is too short.')
        if len(postData['last_name']) < 1:
            errors.append('Last name cannot be blank.')
        if len(postData['last_name']) <3:
            errors.append('Last name is too short.')
        if len(postData['email']) < 1:
            errors.append('Email cannot be blank.')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Email is in invalid format.')
        if len(postData['password']) < 1:
            errors.append('Password cannot be blank.')
        if len(postData['password']) <8:
            errors.append('Password is too short.')
        if not(postData['password'] == postData['password_conf']):
            errors.append('Please correctly confirm Password.')

        if errors:
            return {'errors' : errors}
        else:
            password = postData['password'].encode('utf-8')
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            print hashed
            print len(hashed)
            valid_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashed)
            return {'the_user' : valid_user.id}

    def login(self, postData):
            print '***LOGIN ATTEMPTED***'
            errors = []
            login_user = User.objects.filter(email = postData['email'])
            if not login_user:
                errors.append('Email not registered.')
            else:
                password_check = postData['password']
                stored_password = login_user[0].password
                if not bcrypt.hashpw(password_check.encode('utf-8'), stored_password.encode('utf-8')) == stored_password:
                    errors.append('Password is incorrect.')
            if errors:
                return {'errors' : errors}
            else:
                return {'the_user' : login_user[0].id}

class SecretManager(models.Manager):
    def new_secret(self, postData, user):
        print "***NEW SECRET INITIALISED***"
        errors = []
        if len(postData['content']) <1:
            errors.append('Secret is blank.')
        if errors:
            return {'errors' : errors}
        else:
            valid_secret = Secret.objects.create(content=postData['content'], user_id=user)
            print valid_secret.user_id
            return {'the_secret' : valid_secret}

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Secret(models.Model):
    content = models.TextField(max_length=255)
    user_id = models.ForeignKey(User, related_name="authors")
    likes = models.ManyToManyField(User, related_name="likers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SecretManager()
