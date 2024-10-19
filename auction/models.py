# auction/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("auction:category_detail", args=[self.slug])


class Auction(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auctions"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="auctions"
    )
    photo = models.ImageField(upload_to="media/auctions/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_auctions",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Проверяем, существует ли уже слаг
            while Auction.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"  # Добавляем счетчик к слагу
                counter += 1
            self.slug = slug

        if not self.end_time:
            self.end_time = self.created_at + timedelta(days=3)

        if not self.current_price:
            self.current_price = self.starting_price
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("auction:auction_detail", args=[self.slug])

    @property
    def is_ended(self):
        return timezone.now() >= self.end_time

    def clean(self):
        if self.end_time and self.end_time <= timezone.now():
            raise ValidationError("End time must be in the future")

    def deactivate_auction(self):
        """Deactivate auction after the end time."""
        if self.is_ended:
            self.is_active = False
            self.save()


class Bid(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids"
    )
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-amount"]

    def __str__(self):
        return f"{self.user.email} bid ${self.amount} on {self.auction.name}"

    def save(self, *args, **kwargs):
        if not self.auction:
            raise ValidationError("Bid must be associated with an auction.")

        if self.auction.is_ended:
            raise ValidationError("This auction has ended")

        if self.user == self.auction.author:
            raise ValidationError("You cannot bid on your own auction")

        if self.amount <= self.auction.current_price:
            raise ValidationError("Bid must be higher than current price")

        if self.user.balance < self.amount:
            raise ValidationError("Insufficient balance")

        super().save(*args, **kwargs)

class Quiz(models.Model):
    date = models.DateField(unique=True)
    questions = models.JSONField()

class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)
