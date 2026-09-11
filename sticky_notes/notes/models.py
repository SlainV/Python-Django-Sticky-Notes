from django.db import models


class Note(models.Model):
    # id automatically used as primary key field
    title = models.CharField(max_length=100)
    content = models.TextField()
    color = models.CharField(max_length=7, default="#d2691e")
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title
