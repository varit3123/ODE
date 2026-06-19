from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField("ФИО", max_length=150)
    birth_date = models.DateField("Дата рождения")
    phone = models.CharField("Телефон", max_length=30)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.full_name


class Application(models.Model):
    STATUS_NEW = "Новая"
    STATUS_PROGRESS = "Идет обучение"
    STATUS_DONE = "Обучение завершено"

    STATUS_CHOICES = [
        (STATUS_NEW, STATUS_NEW),
        (STATUS_PROGRESS, STATUS_PROGRESS),
        (STATUS_DONE, STATUS_DONE),
    ]

    TRANSPORT_CHOICES = [
        ("Катер", "Катер"),
        ("Круизный лайнер", "Круизный лайнер"),
        ("Яхта", "Яхта"),
    ]

    PAYMENT_CHOICES = [
        ("Банковская карта", "Банковская карта"),
        ("Наличные в офисе", "Наличные в офисе"),
        ("Безналичный расчет", "Безналичный расчет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    transport = models.CharField("Вид транспорта", max_length=40, choices=TRANSPORT_CHOICES)
    start_date = models.DateField("Дата начала обучения")
    payment_method = models.CharField("Способ оплаты", max_length=60, choices=PAYMENT_CHOICES)
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField("Статус", max_length=40, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.user.username}: {self.transport}"

    @property
    def review_text(self):
        review = getattr(self, "review", None)
        return review.text if review else ""


class Review(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField("Отзыв")
    created_at = models.DateField("Дата отзыва", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв к заявке #{self.application_id}"
