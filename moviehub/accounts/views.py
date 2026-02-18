from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomProfileEditForm, CusProfEditForm
from .models import User, UserProfile


class RegisterView(View):
    """registrování nového uživatele."""
    def get(self,request):
        """zobrazí formular"""
        return render(request, "accounts/register.html")

    def post(self,request):
        """zpracuje registraci a přihlásí uživatele."""
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Hesla se neshodují!!!")
            context = {"username": username, "email": email}
            return render(request, "accounts/register.html", context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Uživatelské jméno již existuje!!!")
            context = {"username": username, "email": email}
            return render(request, "accounts/register.html", context)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        messages.success(request, "Registrace proběhla úspěšně.")
        return redirect("all_movies")

@login_required
def logout_view(request):
    """Odhlaseni uzivatele a redirect na seznam vsech filmů"""
    logout(request)
    messages.info(request, "Byl jsi úspěšně odhlášen.")
    return redirect("all_movies")

@login_required
def profile(request):
    """Zobrazí detail profilu přihlášeného uživatele."""
    context = {"user": request.user}
    return render(request, "accounts/profile.html",context)


@method_decorator(login_required, name="dispatch")
class CustomProfileEdit(View):
    """Zobrazí view pro upravu username/email přes User model"""
    def get(self, request):
        """Zobrazí formular pro upravu username/email"""
        form = CustomProfileEditForm(instance=request.user)
        context = {"form":form}
        return render(request, "accounts/profile_edit_user.html",context)

    def post(self,request):
        """Zpracuje formular"""

        form = CustomProfileEditForm(request.POST, instance=request.user)

        if form.is_valid():
            """kontrola unikat. username udelane ve form/clean()"""
            form.save()
            messages.success(request, "Profil (\"jméno\" a \"email\" byl uspěšně upraven .")
            return redirect("profile")

        # pokud form ne-ok zustanou chyby + puvodni data
        context = {"form":form}
        return render(request, "accounts/profile_edit_user.html",context)

@method_decorator(login_required, name="dispatch")
class CustomProfileEdit2(View):
    """ View pro upravu bio/avatar """
    def get(self, request):
        """ form pro bio/avatar """
        profile, _created = UserProfile.objects.get_or_create(user=request.user)
        form = CusProfEditForm(instance=profile)
        context = {"form":form}
        return render(request, "accounts/profile_edit.html",context)

    def post(self, request):
        """ Zpracuje form bio/avatar """
        profile, _created = UserProfile.objects.get_or_create(user=request.user)
        form = CusProfEditForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profil \"bio\" a \"avatar\" byl uspěšně upraven (ver.2.0).")
            return redirect("profile")

        context = {"form": form}
        return render(request, "accounts/profile_edit.html", context)
