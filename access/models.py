from django.db import models


from django.contrib.auth.models import User
from score.models import Match, Player, Team

# Permissions for users

class AccessPermission(models.Model):
    ACCESS_TYPE = (
        ('R', 'Read-only'),
        ('W', 'Write'),
    )

    main_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='granted_permissions'
    )  # Owner of the resource
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='permissions'
    )  # User with access
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='permissions', null=True, blank=True
    )
    access_type = models.CharField(max_length=1, choices=ACCESS_TYPE, default='R')
    active = models.BooleanField(default=True)
    granted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.access_type} access to {self.match or self.player or self.team}"



# Access requests from users

class AccessRequest(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )

    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='access_requests'
    )
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='access_requests', null=True, blank=True
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='access_requests', null=True, blank=True
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='access_requests', null=True, blank=True
    )
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} requests {self.match or self.player or self.team} ({self.status})"

