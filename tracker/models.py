from django.db import models

COLOR_CHOICES = (
    ('cat1', 'Cat1'),
    ('cat2', 'Cat2'),
    ('cat3', 'Cat3'),
    ('cat4', 'Cat4'),
    ('cat5', 'Cat5'),
)


class Item(models.Model):
    name = models.CharField(max_length=200, null=True)  # Item name
    price = models.IntegerField(null=True)  # price name
    image = models.FileField(blank=True, null=True)  # image field
    categories = models.CharField(max_length=6, choices=COLOR_CHOICES, default='green')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # created time

    def __str__(self):  # returns name of item on reference
        return self.name
