from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class Lesson(models.Model):
    topic = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    parent_lesson = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if self.parent_lesson and self.parent_lesson.parent_lesson:
            raise ValidationError("Max depth level exceeded")
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.topic} ({self.pk})'


class UserLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f'{self.user.username} ({self.lesson.topic})'
