# myapp/subapp/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from accounts.models import UserProfile


class Challenge(models.Model):
    title = models.CharField(max_length=200)
    task = models.TextField()
    image = models.ImageField(upload_to='challenges_images/', default='challenges_images/logo.png')
    deadline = models.DateField(default="2024-12-31")

    def __str__(self):
        return self.title


@receiver(post_migrate)
def create_sample_challenges(sender, **kwargs):
    if Challenge.objects.filter(title="Kids' Tree Planting Challenge").exists():
        return  # Skip creation if samples already exist

    # Create sample challenges if they don't exist
    Challenge.objects.create(
        title="Kids' Tree Planting Challenge",
        task="Help your child plant a tree! Upload a picture of the activity.",
        image='challenges_images/plant.jpg'  # Update with correct image path
    )

    Challenge.objects.create(
        title="Reusable Bag Challenge",
        task="Help keep our environment clean! Buy a reusable bag and carry it around. Upload a picture of it.",
        image='challenges_images/reusable.jpeg'  # Update with correct image path
    )


class AcceptedChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class CompletedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='completed_tasks/')
    caption = models.TextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} completed {self.challenge}'


class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.total_points} points"


class LikedTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(CompletedTask, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} likes {self.task.title}"
