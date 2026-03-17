from django.shortcuts import render
from .models import Challenge

def challenge_list(request):
    # Grab all challenges from the database, ordered by newest first
    challenges = Challenge.objects.all().order_by('-created_at')
    
    # Package them up in a dictionary so our HTML can read them
    context = {
        'challenges': challenges
    }
    
    # Send the data to an HTML template (we will build this next!)
    return render(request, 'qanda/challenge_list.html', context)