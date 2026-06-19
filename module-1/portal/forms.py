import re
from datetime import date

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction

from .models import Application, Profile, Review


BAD_NAME_WORDS = {
    "admin",
    "qwerty",
    "test",
    "user",
    "админ",
    "имя",
    "пользователь",
    "тест",
    "фио",
    "фамилия",
}


class LoginForm(forms.Form):
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        login = cleaned.get("login")
        password = cleaned.get("password")
        if login and password:
            user = authenticate(username=login, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
            cleaned["user"] = user
        return cleaned


class RegistrationForm(forms.Form):
    full_name = forms.CharField(label="ФИО", max_length=150)
    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    phone = forms.CharField(label="Телефон", max_length=30)
    email = forms.EmailField(label="E-mail")
    login = forms.CharField(label="Логин", max_length=60)
    password = forms.CharField(label="Пароль", min_length=8, widget=forms.PasswordInput)

    def clean_full_name(self):
        value = " ".join(self.cleaned_data["full_name"].split())
        parts = value.split()
        if len(parts) < 2 or len(parts) > 3:
            raise forms.ValidationError("Укажите фамилию и имя, при необходимости отчество.")

        checked_parts = []
        for part in parts:
            normalized = "-".join(piece.capitalize() for piece in part.split("-"))
            plain = normalized.replace("-", "").lower()
            if plain in BAD_NAME_WORDS:
                raise forms.ValidationError("Укажите настоящее ФИО, без тестовых значений.")
            if len(set(plain)) == 1:
                raise forms.ValidationError("ФИО не должно состоять из повторяющихся символов.")
            if not re.fullmatch(r"[А-ЯЁ][а-яё]{1,}(?:-[А-ЯЁ][а-яё]{1,})?", normalized):
                raise forms.ValidationError("ФИО должно содержать только русские буквы.")
            checked_parts.append(normalized)
        return " ".join(checked_parts)

    def clean_birth_date(self):
        value = self.cleaned_data["birth_date"]
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if value > today:
            raise forms.ValidationError("Дата рождения не может быть в будущем.")
        if age < 14:
            raise forms.ValidationError("Возраст должен быть не меньше 14 лет.")
        if age > 100:
            raise forms.ValidationError("Проверьте дату рождения.")
        return value

    def clean_phone(self):
        digits = re.sub(r"\D", "", self.cleaned_data["phone"])
        if len(digits) == 10:
            digits = "7" + digits
        if len(digits) == 11 and digits.startswith("8"):
            digits = "7" + digits[1:]
        if len(digits) != 11 or not digits.startswith("7"):
            raise forms.ValidationError("Введите российский номер телефона в формате +7XXXXXXXXXX.")
        if len(set(digits[-10:])) <= 2:
            raise forms.ValidationError("Введите реальный номер телефона.")
        return "+" + digits

    def clean_password(self):
        value = self.cleaned_data["password"]
        if re.search(r"\s", value):
            raise forms.ValidationError("Пароль не должен содержать пробелы.")
        if not re.search(r"[A-Za-zА-Яа-я]", value) or not re.search(r"\d", value):
            raise forms.ValidationError("Пароль должен содержать буквы и цифры.")
        return value

    def clean_login(self):
        value = self.cleaned_data["login"].strip()
        if not re.fullmatch(r"(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}", value):
            raise forms.ValidationError("Логин: латинские буквы и цифры, минимум 6 символов.")
        if User.objects.filter(username__iexact=value).exists():
            raise forms.ValidationError("Этот логин уже занят.")
        return value

    @transaction.atomic
    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["login"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data["full_name"],
            birth_date=self.cleaned_data["birth_date"],
            phone=self.cleaned_data["phone"],
        )
        return user


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("transport", "start_date", "payment_method", "comment")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }


class MobileApplicationForm(ApplicationForm):
    start_date = forms.DateField(
        label="Дата начала обучения",
        input_formats=["%d.%m.%Y"],
        widget=forms.TextInput(attrs={"placeholder": "ДД.ММ.ГГГГ", "maxlength": "10"}),
        error_messages={"invalid": "Введите дату в формате ДД.ММ.ГГГГ."},
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("text",)
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}


class AdminLoginForm(forms.Form):
    login = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("login") != "Admin26" or cleaned.get("password") != "Demo20":
            raise forms.ValidationError("Неверный логин или пароль администратора.")
        return cleaned
