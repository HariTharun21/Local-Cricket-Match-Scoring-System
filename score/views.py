from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Player, Team, Match, Over ,PlayerMatchStats
from .forms import PlayerForm, PlayerSearchForm, TeamForm, MatchForm
from django.http import JsonResponse, HttpResponse
import json
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ErrorReportForm
from .servicenow_client import create_error_record

from django.contrib.auth.mixins import LoginRequiredMixin
from access.models import AccessPermission

# -------------------------------
# Helper function to check permissions
# -------------------------------
def has_permission(user, obj, perm_type='R'):
    if user == getattr(obj, 'user', None) or user.is_superuser:
        return True
    perms = AccessPermission.objects.filter(user=user, access_type=perm_type, active=True)
    if isinstance(obj, Match):
        return perms.filter(match=obj).exists()
    elif isinstance(obj, Player):
        return perms.filter(player=obj).exists()
    elif isinstance(obj, Team):
        return perms.filter(team=obj).exists()
    return False



class HomeView(LoginRequiredMixin, View):
    login_url = "login"
    def get(self, request):
        return render(request, 'base.html')


class PlayerListView(View):
    def get(self, request):
        players = Player.objects.all()

         # Filter by read access
        players = [p for p in players if has_permission(request.user, p, 'R')]


        search_form = PlayerSearchForm(request.GET or None)
        add_form = PlayerForm()

        if search_form.is_valid():
            name = search_form.cleaned_data.get('name')
            if name:
                players = players.filter(name__icontains=name)

        return render(request, 'player_list.html', {
            'players': players,
            'search_form': search_form,
            'add_form': add_form,
        })

    def post(self, request):
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user  # assign the creator
            player.save()               # SAVE first!

        # Now player is saved, check write permission
            if has_permission(request.user, player, 'W') or request.user.is_superuser:
                messages.success(request, "Player created successfully.")
            else:
                messages.error(request, "You don't have permission to create a player.")
                player.delete()  # rollback if no permission

        return redirect('player_list')



class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player_form.html'
    success_url = reverse_lazy('player_list')


class PlayerUpdateView(LoginRequiredMixin,UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'player_form.html'
    success_url = reverse_lazy('player_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not has_permission(request.user, obj, 'W'):
            messages.error(request, "You don't have write access to update this player.")
            return redirect('player_list')
        return super().dispatch(request, *args, **kwargs)


class PlayerDeleteView(LoginRequiredMixin,DeleteView):
    model = Player
    template_name = 'player_confirm_delete.html'
    success_url = reverse_lazy('player_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not has_permission(request.user, obj, 'W'):
            messages.error(request, "You don't have permission to delete this player.")
            return redirect('player_list')
        return super().dispatch(request, *args, **kwargs)



class TeamListView(LoginRequiredMixin,ListView):
    model = Team
    template_name = 'team_list.html'
    context_object_name = 'teams'
    def get_queryset(self):
        qs = super().get_queryset()
        return [t for t in qs if has_permission(self.request.user, t, 'R')]


class TeamCreateView(LoginRequiredMixin,CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_form.html'
    success_url = reverse_lazy('team_list')
    def form_valid(self, form):
        team = form.save(commit=False)
        team.user = self.request.user
        team.save()
        messages.success(self.request, "Team created successfully.")
        return super().form_valid(form)


   

class TeamPlayersView(View):
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        player_list = Player.objects.exclude(teams__isnull=False).union(team.players.all())
        return render(request, 'team_players.html', {
            'team': team,
            'player_list': player_list
        })

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        selected_player_ids = request.POST.getlist('players')
        team.players.set(selected_player_ids)
        return redirect('team_list')


class TeamDeleteView(LoginRequiredMixin,DeleteView):
    model = Team
    template_name = 'team_confirm_delete.html'
    success_url = reverse_lazy('team_list')
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not has_permission(request.user, obj, 'W'):
            messages.error(request, "You don't have permission to delete this team.")
            return redirect('team_list')
        return super().dispatch(request, *args, **kwargs)


class MatchListView(LoginRequiredMixin,ListView):
    model = Match
    template_name = 'match_list.html'
    context_object_name = 'matches'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return [m for m in qs if has_permission(self.request.user, m, 'R')]


class MatchCreateView(LoginRequiredMixin,View):
    def get(self, request):
        last_match = Match.objects.order_by('-match_number').first()
        next_match_number = last_match.match_number + 1 if last_match else 1
        form = MatchForm(initial={'match_number': next_match_number})
        return render(request, 'match_form.html', {'form': form})
    

    def post(self, request):
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.user = request.user
            match.save()
            overs_no = form.cleaned_data['total_overs']
            request.session['total_overs'] = overs_no
            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']
            request.session['total_overs'] = overs_no
            request.session['team1'] = team1.id
            request.session['team2'] = team2.id
            return redirect('toss_decision', match_id=match.pk)
        return render(request, 'match_form.html', {'form': form})


class MatchDeleteView(LoginRequiredMixin, DeleteView):
    model = Match
    template_name = 'match_confirm_delete.html'
    success_url = reverse_lazy('match_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not has_permission(request.user, obj, 'W'):
            messages.error(request, "You don't have permission to delete this match.")
            return redirect('match_list')
        return super().dispatch(request, *args, **kwargs)


class TossDecisionView(View):
    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        return render(request, 'toss.html', {'match': match})

    def post(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        toss_winner_id = request.POST.get('toss_winner')
        decision = request.POST.get('decision')

        if not toss_winner_id or not decision:
            messages.error(request, "Please select a team and a decision.")
            return redirect('toss_decision', match_id=match_id)

        try:
            toss_winner_id = int(toss_winner_id)
        except ValueError:
            messages.error(request, "Invalid toss winner.")
            return redirect('toss_decision', match_id=match_id)

        toss_winner = get_object_or_404(Team, id=toss_winner_id)
        opponent_team = match.team1 if toss_winner != match.team1 else match.team2

        # Decide batting/bowling based on toss decision
        if decision.lower() == "bat":
            batting_team = toss_winner
            bowling_team = opponent_team
        else:  # bowl first
            batting_team = opponent_team
            bowling_team = toss_winner

        # Save in session
        request.session['batting_team_id'] = batting_team.id
        request.session['bowling_team_id'] = bowling_team.id
        request.session['toss_winner_id'] = toss_winner_id
        request.session['toss_decision'] = decision
        request.session['match_id'] = match.id

        messages.success(request, "Toss decision saved.")
        return redirect('basic_over_create', match_id=match.id)
    

class BasicOverCreationView(View):
    def get(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)
        
        batting_team_id = request.session.get('batting_team_id')
        bowling_team_id = request.session.get('bowling_team_id')

        if not batting_team_id or not bowling_team_id:
            messages.error(request, "Teams not set in session. Please redo toss.")
            return redirect('toss_decision', match_id=match.id)

        batting_team = Team.objects.get(id=batting_team_id)
        bowling_team = Team.objects.get(id=bowling_team_id)

        context = {
            'match': match,
            'batters': batting_team.players.all(),
            'bowlers': bowling_team.players.all(),
        }
        return render(request, 'basic_over_creation.html', context)

    def post(self, request, match_id):
        match = get_object_or_404(Match, id=match_id)

        striker_id = request.POST.get('striker')
        non_striker_id = request.POST.get('non_striker')
        bowler_id = request.POST.get('bowler')

        

        # Save Over object
        over = Over.objects.create(
            match_no=match,
            bowling_team=Team.objects.get(id=request.session.get('bowling_team_id')),
            over_no=1,  # ✅ automatic number
            bowler=Player.objects.get(id=bowler_id),
            runs=0,
            wickets=0,
            over_summary="",
            user=request.user
        )

        return redirect(
            'over_score',
            match_id=match.id,
            over_id=over.id,
            striker_id=striker_id,
            non_striker_id=non_striker_id,
            bowler_id=bowler_id
        )





class OverListView(ListView):
    model = Over
    template_name = 'over_scoring_ui.html'
    context_object_name = 'overs'





class OverScoreView(LoginRequiredMixin,View):
    def get(self, request, match_id, over_id, striker_id, non_striker_id, bowler_id):
        match = get_object_or_404(Match, id=match_id)
        if not has_permission(request.user, match, 'R'):
            messages.error(request, "You don't have access to this match.")
            return redirect('match_list')

        batting_team_id = request.session.get('batting_team_id')
        bowling_team_id = request.session.get('bowling_team_id')

        if not batting_team_id or not bowling_team_id:
            messages.error(request, "Teams not set in session. Please redo toss.")
            return redirect('toss_decision', match_id=match.id)

        batting_team = get_object_or_404(Team, id=batting_team_id)
        bowling_team = get_object_or_404(Team, id=bowling_team_id)

        bowler_list = bowling_team.players.all()
        striker_obj = get_object_or_404(Player, id=striker_id)
        striker,_ = PlayerMatchStats.objects.get_or_create(player=striker_obj, match=match, user=request.user)
        non_striker_obj = get_object_or_404(Player, id=non_striker_id)
        non_striker,_ = PlayerMatchStats.objects.get_or_create(player=non_striker_obj, match=match, user=request.user)
        bowler = get_object_or_404(Player, id=bowler_id)
        request.session["bowler_id"]=bowler_id

        if "batter_list" not in request.session:
            batter_list = batting_team.players.exclude(id__in=[striker_obj.id, non_striker_obj.id])
            request.session['batter_list'] = list(batter_list.values_list("id", flat=True))
            request.session['outed_players'] = []

        batter_ids = request.session.get('batter_list', [])
        outed_players = request.session.get('outed_players', [])

        remaining_batters = Player.objects.filter(id__in=batter_ids).exclude(id__in=outed_players)
        
        over = get_object_or_404(Over, id=over_id)
        total_overs = request.session.get('total_overs')
        overs = Over.objects.filter(match_no=match).order_by('over_no')

        return render(request, 'over_scoring_ui.html', {
            'match': match,
            'total_overs': total_overs,
            'over': over,
            'overs': overs,
            'striker': striker_obj,
            'non_striker': non_striker_obj,
            'bowler_list': bowler_list,
            'bowler': bowler,
            'remaining_batters': remaining_batters,
            'outed_players': Player.objects.filter(id__in=outed_players)
        })

    def post(self, request, match_id, over_id):
        match = get_object_or_404(Match, id=match_id)
        over = get_object_or_404(Over, id=over_id)

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        striker_id = data.get("striker_id")
        non_striker_id = data.get("non_striker_id")
        bowler_id = data.get("bowler_id")
        event = data.get("event")
        runs = int(event) if str(event).isdigit() else 0
        
       

        print("Received data:", data)

        if not all([striker_id, non_striker_id, bowler_id, event]):
            return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

        if not has_permission(request.user, match, "W"):
            return JsonResponse({"status": "error", "message": "No write access"}, status=403)

        striker = get_object_or_404(Player, id=striker_id)
        bowler_id=request.session.get("bowler_id")
        non_striker = get_object_or_404(Player, id=non_striker_id)
        bowler = get_object_or_404(Player, id=bowler_id)
        striker_stats, _ = PlayerMatchStats.objects.get_or_create(
        match=match,
        player_id=striker_id,
        defaults={"user": request.user}
        )
        bowler_stats, _ = PlayerMatchStats.objects.get_or_create(
        match=match,
        player_id=bowler_id,
        defaults={"user": request.user}
           )


    #  Handle scoring events (0–6)
        if event in ["0", "1", "2", "3", "4", "6"]:
            
            

            striker_stats.runs += runs
            striker_stats.balls += 1
            striker_stats.save()

            bowler_stats.bowling_runs += runs
            bowler_stats.overs_bowled += 0.1
            bowler_stats.save()

            over.runs += runs
            over.save()

            return JsonResponse({"status": "success", "message": f"{runs} run(s) added"})

    #  Handle wicket event
        elif event == "W":
            outed_player_data = data.get("outed_player", {})
            player_id = outed_player_data.get("player_id", striker_id)

            over.wickets += 1
            over.save()

            striker_stats = PlayerMatchStats.objects.get(match=match, player_id=player_id)
            striker_stats.balls += 1
            striker_stats.save()

            outed_players = request.session.get("outed_players", [])
            if striker.id not in outed_players:
                outed_players.append(striker.id)
                request.session["outed_players"] = outed_players

            return JsonResponse({"status": "success", "message": "Wicket updated"})

    #  Handle over completion event
        elif event == "OVER":
            over_summary = data.get("over_summary", "")
            new_bowler_id = data.get("new_bowler_id")

            bowler_stats.overs_bowled += 1
            bowler_stats.save()

            over.over_summary = over_summary
            over.save()

            if not new_bowler_id:
                return JsonResponse({"status": "error", "message": "New bowler not specified"}, status=400)

            try:
                new_bowler = Player.objects.get(id=new_bowler_id)
            except Player.DoesNotExist:
                return JsonResponse({"status": "error", "message": "New bowler not found"}, status=404)

            bowling_team = match.team2  

            new_over = Over.objects.create(   
         match_no=match,
         bowling_team=bowling_team,
         over_no=over.over_no + 1,
         bowler=new_bowler,
         runs=0,
         wickets=0,
         over_summary="",
         user=request.user
                       )

    
        request.session["bowler_id"] = new_bowler_id

        return JsonResponse({
        "status": "success",
        "message": "Over submitted successfully",
        "new_over_id": new_over.id,
        "over_summary": over_summary, 
        "over_no" : over.over_no,
        "new_bowler_id": new_bowler.id ,
        "team": str(over.bowling_team)
                 })


    
        
        





class ErrorReportCreateView(FormView):
    template_name = "error_report.html"
    form_class = ErrorReportForm
    success_url = reverse_lazy("error_report_sent")  

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["user_name"] = self.request.user.username or self.request.user.username
            initial["user_email"] = self.request.user.email or self.request.user.email
        
        return initial

    def form_valid(self, form):
        
        user = self.request.user
        payload = {
            "user_name": user.username if user.is_authenticated else form.cleaned_data.get("user_name") or "Anonymous",
            "user_email": user.email if user.is_authenticated else None,
            "where_error": form.cleaned_data["where_error"],
            "description": form.cleaned_data["description"],
            "page_url": form.cleaned_data.get("page_url", ""),
            "severity": form.cleaned_data["severity"],
           
        }

        result = create_error_record(payload)

        if result["ok"]:
            
            messages.success(self.request, "Thanks — your report was sent to our team.")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Failed to send report. We'll retry automatically. (Error logged)")
          
            return super().form_valid(form)
