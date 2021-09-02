from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from pdf2image import*
import os
from .models import *

poppler_path = r"C:\Program Files\poppler-0.68.0\bin"

# Create your views here.
def index(request):
    if request.method == 'POST':
        pdfs = request.FILES.getlist('pdf')
        for pdf in pdfs:
            file = Files.objects.create(user=request.user, pdf=pdf)
            file.save()
            pdftoimages(file)
        return redirect('mybooks')
    else:
        return render(request, "app/index.html")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password = password)
        if user is not None:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, "app/login.html")

def signup(request):
    if request.method == 'POST':
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1'] == request.POST['password2']
        if password:
            user = User.objects.create_user(username = email, email=email, password=request.POST['password1'])
            user.save();
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        else:
            return redirect('signup')
    return render(request, "app/signup.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def mybooks(request):
    if request.user.is_authenticated:
        # print(request.user.id)
        pdfs = Files.objects.filter(user_id=request.user.id)
        # print(pdfs)
        # for i in pdfs:
        #     print(i.id)
        return render(request, "app/mybooks.html",{
            "pdfs": pdfs,
        })
    else:
        return redirect('login')

def profile(request):
    return render(request, "app/profile.html")

def edit(request, id, page):
    return render(request, "app/edit.html")

def pdftoimages(pdf):
    pages = convert_from_path(pdf.pdf.path)
    c = 1
    print("THis ",pdf)
    # for page in pages:
    #     myfile = str(pdf) + str(c) + '.jpg'
    #     c = c + 1
    #     print(myfile)
    # print(type(pdf.pdf.path))
