from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Django's built-in User model


class Team(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams", default=None)  # owner
    name = models.CharField(max_length=30)
    players = models.ManyToManyField('Player', related_name='teams', blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="players",default=None)  # owner
    name = models.CharField(max_length=30, null=False)
    total_runs = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    total_matches = models.IntegerField(default=0)
    total_balls = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches", default=None)  # owner
    match_number = models.IntegerField()
    date = models.DateField(default=timezone.now)
    team1 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='team2_matches')
    winners = models.CharField(max_length=30, blank=True, null=True)
    total_overs = models.PositiveIntegerField(default=2)
    team1_runs = models.IntegerField(default=0)
    team1_wickets = models.IntegerField(default=0)
    team2_runs = models.IntegerField(default=0)
    team2_wickets = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number} - {self.team1.name} vs {self.team2.name} on {self.date}"


class Over(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="overs",default=None)  # owner
    match_no = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="overs")
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="bowling_overs", null=True, blank=True)
    over_no = models.IntegerField()
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    over_summary = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Over {self.over_no} | {self.bowler.name} - Runs: {self.runs}, Wickets: {self.wickets}"


class PlayerMatchStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_match_stats",default=None)  # owner
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="player_stats")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_stats")
   

    runs = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    overs_bowled = models.FloatField(default=0.0)
    bowling_runs = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} in Match {self.match.match_number}"