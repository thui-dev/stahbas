from django.db import models


class Answers(models.Model):
    equipe = models.CharField(max_length=64, default="")
    timestamp = models.DateTimeField("date published")

