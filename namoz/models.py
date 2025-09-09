from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Namoz(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bomdod = models.PositiveIntegerField(default=0)
    peshin = models.PositiveIntegerField(default=0)
    asr = models.PositiveIntegerField(default=0)
    shom = models.PositiveIntegerField(default=0)
    xufton = models.PositiveIntegerField(default=0)
    vitr = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}"

class NamozAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prayer = models.CharField(max_length=20)   # masalan: "bomdod"
    action = models.CharField(max_length=1, choices=[('+', 'Plus'), ('-', 'Minus')])
    old_value = models.PositiveIntegerField()
    new_value = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']