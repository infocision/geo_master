from django.shortcuts import render, HttpResponse
# import pandas as pd
import pymysql


def sign_in_view(request):
    return render(request, 'sign_in.html')


def dashboard(request):
    usr = request.POST['user_name']
    pwd = request.POST['password']

    return render(request, 'dashboard.html')
