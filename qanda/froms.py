from django import forms
from .models import Challenge, Solution

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        # We only want the user to fill out these three fields
        fields = ['title', 'body', 'categories']
        # Adding some basic CSS classes so it doesn't look ugly
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px; margin-bottom: 10px;'}),
            'body': forms.Textarea(attrs={'style': 'width: 100%; height: 150px; padding: 8px;'}),
            'categories': forms.CheckboxSelectMultiple(), # Makes categories a nice list of checkboxes
        }

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'style': 'width: 100%; height: 100px; padding: 8px;', 'placeholder': 'Write your solution here...'}),
        }