from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import CRM_model
from .forms import AddRecord, info_form
# Create your views here.

def home(request):
    records = CRM_model.objects.all()
    return render(request, "crmapp/home.html", {'records': records})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return HttpResponse("Your password and conform password are not the same")
        else:
            user = User.objects.create_user(username, email, password1)
            user.save()
            return redirect("login")

    return render(request, "crmapp/signup.html", {})

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")
    else:
        return render(request, "crmapp/login.html")
    
def logout_user(request):
    logout(request)
    return redirect("home")

def update_info(request, pk):
    info = CRM_model.objects.get(id=pk)
    form = info_form(instance=info)

    if request.method == "POST":
        form = info_form(request.POST, instance=info)
        if form.is_valid():
            form.save()
        return redirect("/")

    context = {
        "info": info,
        "form": form,
        "item": info,
    }
    return render(request, "crmapp/update.html", context)


def delete(request, pk):
    item = CRM_model.objects.get(id=pk)
    context = {'item': item}
    
    if request.method == "POST":
        item.delete()
        return redirect("/")
    
    return render(request, "crmapp/delete.html", context)

def add_record(request):
    form = AddRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                return redirect("home")
        return render(request, "crmapp/add_record.html", {"form" : form})
    else:
        return render(request, "crmapp/add_record.html")