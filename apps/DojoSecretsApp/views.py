# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import User, Secret
from django.contrib import messages
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'DojoSecretsApp/index.html')

def register(request):
    new_user = User.objects.register(request.POST)
    if 'the_user' in new_user:
        request.session['logged_user'] = new_user['the_user']
        messages.success(request, 'You successfully registered!')
        return redirect('/success')
    else:
        for i in new_user['errors']:
            messages.error(request, i)
        return redirect('/')

def login(request):
    if request.method == 'POST':
        login_check = User.objects.login(request.POST)
        if 'the_user' in login_check:
            request.session['logged_user'] = login_check['the_user']
            messages.success(request, 'You successfully logged in!')
            return redirect('/success')
        else:
            for i in login_check['errors']:
                messages.error(request, i)
            return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['logged_user'])
    print user.first_name + " in success"
    context = {
        'logged_in_user' : user
    }
    return redirect(('/secrets'), context)

def secrets(request):
    user = User.objects.get(id=request.session['logged_user'])
    print user.first_name + " in secrets"
    secrets = Secret.objects.order_by('-created_at')[0:5]
    for secret in secrets:
        if user.id in secret.likes.all():
            secret.annotate(liked_by_user)
    #annotate all secrets against user_id to check if they've been liked
    context = {
        'logged_in_user' : user,
        'secrets' : secrets
    }
    return render(request, 'DojoSecretsApp/secrets.html', context)

def new_secret(request):
    user = User.objects.get(id=request.session['logged_user'])
    if request.method == 'POST':
        create_new_secret = Secret.objects.new_secret(request.POST, user)
        return redirect('/secrets')

def delete(request, id):
    secret_for_deletion = Secret.objects.get(id=id).delete()
    return redirect('/secrets')

def like(request, id):
    user = User.objects.get(id=request.session['logged_user'])
    secret_to_like = Secret.objects.get(id=id)
    secret_to_like.likes.add(user)
    return redirect('/secrets')

def popular(request):
    user = User.objects.get(id=request.session['logged_user'])
    popular_secrets = Secret.objects.order_by('-likes').all
    context = {
        'logged_in_user' : user,
        'secrets' : popular_secrets
    }
    return render(request, 'DojoSecretsApp/popular.html', context)

def logout(request):
    request.session['logged_user'] = {}
    return redirect('/')

# Create your views here.
