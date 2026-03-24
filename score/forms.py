from django import forms
from score.models import Player,Team,Match


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_number', 'team1', 'team2','total_overs']  # added total_overs
        widgets = {
            'match_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'team1': forms.Select(attrs={'class': 'form-select team-select'}),
            'team2': forms.Select(attrs={'class': 'form-select team-select'}),
        }
        





class PlayerSearchForm(forms.Form):
    name = forms.CharField(max_length=30, required=False, label='search by name')




SEVERITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
]

class ErrorReportForm(forms.Form):
    where_error = forms.CharField(label="Where did you get the error?", max_length=255, required=True)
    description = forms.CharField(widget=forms.Textarea, label="Describe what happened")
    page_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    severity = forms.ChoiceField(choices=SEVERITY_CHOICES, initial="Medium")
   