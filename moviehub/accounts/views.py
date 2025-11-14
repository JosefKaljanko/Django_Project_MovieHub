# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomProfileEditForm
# update Profile
# from django.views.generic import UpdateView

from .models import User



class RegisterView(View):
    """registrování nového uživatele."""
    def get(self,request):
        return render(request, "accounts/register.html")

    def post(self,request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Hesla se neshodují!!!")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Uživatelské jméno již existuje!!!")
            return render(request, "accounts/register.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Registrace proběhla úspěšně.")
        return redirect("all_movies")

@login_required
def logout_view(request):
    """Odhlaseni uzivatele"""
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("all_movies")

@login_required
def profile(request):
    if request.method == "GET":
        return render(request, "accounts/profile.html",{"user": request.user})

# class ProfileEditView(LoginRequiredMixin, UpdateView):
#     model = User
#     fields = ["username", "email", "bio", "avatar"]
#     template_name =

class CustomProfileEdit(View):
    def get(self,request):
        form = CustomProfileEditForm(instance=request.user)
        context = {"form":form}
        return render(request, "accounts/profile_edit.html",context)
    def post(self,request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        print(username)
        print(email)
        print(bio)

        conttext = {"mes":"dekujeme, data máme, pracujeme na tom..."}
        return render(request, "accounts/profile_edit.html",conttext)
