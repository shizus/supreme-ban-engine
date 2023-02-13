
from django.db import models


class Game(models.Model):
    """ Stores Game's information """
    # This could seem a lot but we live in a world where
    # 'Cthulhu Saves the World: Super Hyper Enhanced Championship Edition' is a real game.
    name = models.CharField(max_length=180, db_index=True)  # not a primary key, two games can have the same name.


REASON_CHOICES = (
    ("FOUL_LANGUAGE", "foul_language"),
    ("CHEATING", "cheating"),
    ("HARASSMENT", "harassment"),
    ("OTHER", "other")
)


class PlayerReport(models.Model):
    """ Stores player's information """

    email = models.EmailField(max_length=254, db_index=True)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    game = models.ForeignKey(to=Game, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

