from django.core.validators import RegexValidator
from django.db import models


hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Enter a valid hexadecimal colour, for example #FF0000.",
)


class Note(models.Model):
    # id automatically used as primary key field
    title = models.CharField(max_length=100)
    content = models.TextField()
    color = models.CharField(
        max_length=7,
        default="#d2691e",
        validators=[hex_color_validator],
    )
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title
