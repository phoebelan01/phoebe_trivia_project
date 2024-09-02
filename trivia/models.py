from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Score(models.Model):
    player = models.ForeignKey(Player, related_name='scores', on_delete=models.CASCADE)
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name}: {self.points} points"

class TriviaQuestion(models.Model):
    theme = models.CharField(max_length=100)
    question = models.CharField(max_length=255)
    options = models.JSONField()
    answer = models.IntegerField()

    def __str__(self):
        return self.question