from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.set_password(form.cleaned_data["password"])
            obj.save()
            return render(request, "home.html")
        else:
            return render(request, "register.html", {"form": form})
    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():
            try:
                db_user = User.objects.get(username=username)
                if db_user.username == username and check_password(password,
                                                                   db_user.password)  and db_user.is_active:
                    login(request, db_user)
                    return redirect("/")
                else:
                    return render(request, 'login.html', {'form': form})
            except Exception as e:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})

    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.user:
        logout(request)
    return redirect("")