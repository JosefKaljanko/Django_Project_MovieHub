# from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomProfileEditForm, CusProfEditForm
# update Profile
# from django.views.generic import UpdateView

from .models import User, UserProfile


class RegisterView(View):
    """registrování nového uživatele."""
    def get(self,request):
        # pozdeji form bootstrap
        return render(request, "accounts/register.html")

    def post(self,request):
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
    """Odhlaseni uzivatele"""
    logout(request)
    messages.info(request, "Byl jsi úspěšně odhlášen.")
    return redirect("all_movies")

@login_required
def profile(request):
    """Detail profilu přihlášeného uživatele."""
    context = {"user": request.user}
    return render(request, "accounts/profile.html",context)

# class ProfileEditView(LoginRequiredMixin, UpdateView):
#     model = User
#     fields = ["username", "email", "bio", "avatar"]
#     template_name =

class CustomProfileEdit(View):
    def get(self, request):
        form = CustomProfileEditForm(instance=request.user)
        context = {"form":form}
        return render(request, "accounts/profile_edit_user.html",context)

    def post(self,request):
        # username = request.POST.get("username")
        # bio = request.POST.get("bio")
        # print(username)
        # print(bio)
        # if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
        #     print(f"{username} is already registered.")
        #     return render(request, "accounts/profile_edit.html",context={"form":CustomProfileEditForm(), "mes":"Username už existuje!!"})
        #
        # conttext = {"mes":"dekujeme, data máme, pracujeme na tom..."}
        # return render(request, "accounts/profile_edit.html",conttext)

        form = CustomProfileEditForm(
            request.POST,
            # request.FILES,
            instance=request.user
        )

        if form.is_valid():
            # kontrola unikat. username idelane ve form/clean()
            form.save()
            messages.success(request, "Profil (\"jméno\" a \"email\" byl uspěšně upraven .")
            return redirect("profile")

        # pokud form ne-ok zustanou chyby + puvodni data
        context = {"form":form}
        return render(request, "accounts/profile_edit_user.html",context)

@method_decorator(login_required, name="dispatch")    # ??????
class CustomProfileEdit2(View):
    """
    druha varianta upravy prof. - jiny form(avatar,bio...)
    """
    def get(self, request):
        # form = CustomProfileEditForm(instance=request.user)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = CusProfEditForm(instance=profile)
        context = {"form":form}
        return render(request, "accounts/profile_edit.html",context)

    def post(self, request):
        # username = request.POST.get("username")
        # bio = request.POST.get("bio")
        # print(username)
        # print(bio)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = CusProfEditForm(
            request.POST,
            request.FILES,
            # instance=request.user.userprofile,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profil \"bio\" a \"avatar\" byl uspěšně upraven (ver.2.0).")
            return redirect("profile")

        context = {"form": form}
        return render(request, "accounts/profile_edit.html", context)
