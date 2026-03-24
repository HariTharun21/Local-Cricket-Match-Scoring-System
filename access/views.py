
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from .models import AccessRequest, AccessPermission
from score.models import Match, Player, Team
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# User requests access to a resource

def request_access(request, match_id=None, player_id=None, team_id=None):
    if not request.user.is_authenticated:
        messages.error(request, "You need to login to request access.")
        return redirect('login')

    match = Match.objects.get(id=match_id) if match_id else None
    player = Player.objects.get(id=player_id) if player_id else None
    team = Team.objects.get(id=team_id) if team_id else None

    # Check if user already requested
    if AccessRequest.objects.filter(requester=request.user, match=match, player=player, team=team).exists():
        messages.info(request, "You have already requested access.")
    else:
        AccessRequest.objects.create(
            requester=request.user,
            match=match,
            player=player,
            team=team
        )
        messages.success(request, "Access request sent to the main user.")

    return redirect('home')



# Main user manages pending requests

def manage_requests(request, match_id=None, player_id=None, team_id=None):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch pending requests for the given resource
    if match_id:
        resource_requests = AccessRequest.objects.filter(match_id=match_id, status='P')
    elif player_id:
        resource_requests = AccessRequest.objects.filter(player_id=player_id, status='P')
    elif team_id:
        resource_requests = AccessRequest.objects.filter(team_id=team_id, status='P')
    else:
        resource_requests = []

    # Handle POST actions (approve/reject)
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')  # 'approve' or 'reject'
        access_request = get_object_or_404(AccessRequest, id=req_id)

        # Verify main user permission
        perm = None
        if access_request.match:
            perm = AccessPermission.objects.filter(match=access_request.match, user=request.user, access_type='W', active=True).first()
        elif access_request.player:
            perm = AccessPermission.objects.filter(player=access_request.player, user=request.user, access_type='W', active=True).first()
        elif access_request.team:
            perm = AccessPermission.objects.filter(team=access_request.team, user=request.user, access_type='W', active=True).first()

        if not perm and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to approve/reject requests.")

        # Approve request
        if action == 'approve':
            access_request.status = 'A'
            AccessPermission.objects.create(
                main_user=request.user,
                user=access_request.requester,
                match=access_request.match,
                player=access_request.player,
                team=access_request.team,
                access_type='R',  # default read-only
                active=True
            )
            messages.success(request, f"Access granted to {access_request.requester.username}.")
        # Reject request
        elif action == 'reject':
            access_request.status = 'R'
            messages.info(request, f"Access request from {access_request.requester.username} rejected.")

        access_request.save()

    return render(request, 'access/manage_requests.html', {'requests': resource_requests})

