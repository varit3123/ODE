from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from portal.forms import AdminLoginForm, ApplicationForm, LoginForm, RegistrationForm, ReviewForm
from portal.models import Application, Review


def user_applications(user):
    return (
        Application.objects.filter(user=user)
        .select_related("review")
        .order_by("-created_at", "-id")
    )


def admin_applications():
    return Application.objects.select_related("user", "user__profile").order_by("-created_at", "-id")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("module1:cabinet")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        return redirect("module1:cabinet")
    return render(request, "module1/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("module1:cabinet")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Регистрация выполнена.")
        return redirect("module1:cabinet")
    return render(request, "module1/register.html", {"form": form})


@login_required(login_url="module1:login")
def cabinet_view(request):
    if request.method == "POST":
        application = get_object_or_404(Application, pk=request.POST.get("application_id"), user=request.user)
        if application.status != Application.STATUS_DONE:
            raise PermissionDenied("Отзыв доступен только после завершения обучения.")
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                application=application,
                defaults={"user": request.user, "text": form.cleaned_data["text"]},
            )
            messages.success(request, "Отзыв сохранен.")
            return redirect("module1:cabinet")
    return render(
        request,
        "module1/cabinet.html",
        {"applications": user_applications(request.user), "review_form": ReviewForm()},
    )


@login_required(login_url="module1:login")
def request_view(request):
    form = ApplicationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.user = request.user
        application.status = Application.STATUS_NEW
        application.save()
        messages.success(request, "Заявка принята.")
        return redirect("module1:cabinet")
    return render(request, "module1/request.html", {"form": form})


def admin_view(request):
    form = AdminLoginForm()
    if request.method == "POST" and request.POST.get("action") == "login":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            request.session["module1_admin"] = True
            return redirect("module1:admin")
    elif request.method == "POST" and request.session.get("module1_admin"):
        application = get_object_or_404(Application, pk=request.POST.get("application_id"))
        application.status = request.POST.get("status", application.status)
        application.save(update_fields=["status"])
        messages.success(request, "Статус изменен.")
        return redirect("module1:admin")

    applications = admin_applications() if request.session.get("module1_admin") else []
    return render(request, "module1/admin.html", {"form": form, "applications": applications})


def logout_view(request):
    logout(request)
    return redirect("module1:login")
