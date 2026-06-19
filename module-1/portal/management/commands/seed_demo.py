from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from portal.models import Application, Profile, Review


class Command(BaseCommand):
    help = "Creates demo users and applications for the exam project."

    def handle(self, *args, **options):
        demo = self.create_user(
            username="demo26",
            password="Demo2026",
            email="demo@vodit.ru",
            full_name="Иванов Петр Сергеевич",
            birth_date=date(2001, 4, 12),
            phone="+7 900 125-45-67",
        )
        anna = self.create_user(
            username="anna26",
            password="River2026",
            email="anna@vodit.ru",
            full_name="Смирнова Анна Олеговна",
            birth_date=date(2000, 10, 3),
            phone="+7 911 333-21-10",
        )

        first = self.create_application(
            user=demo,
            transport="Катер",
            start_date=date(2026, 7, 2),
            payment_method="Банковская карта",
            comment="Удобно вечером.",
            status=Application.STATUS_NEW,
        )
        done = self.create_application(
            user=demo,
            transport="Яхта",
            start_date=date(2026, 7, 18),
            payment_method="Наличные в офисе",
            comment="",
            status=Application.STATUS_DONE,
        )
        self.create_application(
            user=anna,
            transport="Круизный лайнер",
            start_date=date(2026, 8, 4),
            payment_method="Безналичный расчет",
            comment="Нужны документы для организации.",
            status=Application.STATUS_PROGRESS,
        )

        Review.objects.get_or_create(
            application=done,
            defaults={
                "user": demo,
                "text": "Курс помог уверенно выполнять базовые маневры.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))

    def create_user(self, username, password, email, full_name, birth_date, phone):
        user, _ = User.objects.get_or_create(username=username, defaults={"email": email})
        user.email = email
        user.set_password(password)
        user.save()
        Profile.objects.update_or_create(
            user=user,
            defaults={"full_name": full_name, "birth_date": birth_date, "phone": phone},
        )
        return user

    def create_application(self, user, transport, start_date, payment_method, comment, status):
        application, _ = Application.objects.get_or_create(
            user=user,
            transport=transport,
            start_date=start_date,
            defaults={"payment_method": payment_method, "comment": comment, "status": status},
        )
        application.payment_method = payment_method
        application.comment = comment
        application.status = status
        application.save()
        return application
