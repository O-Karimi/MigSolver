from django.shortcuts import render, get_object_or_404
from .models import Challenge

def challenge_list(request):
    challenges = Challenge.objects.all().order_by('-created_at')
    context = {'challenges': challenges}
    return render(request, 'qanda/challenge_list.html', context)

def challenge_detail(request, challenge_id):
    # Fetch the specific challenge, or throw a 404 error if it doesn't exist
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    # Fetch all solutions linked to this challenge. 
    # We order by '-is_accepted' to push the correct answer to the top!
    solutions = challenge.solutions.all().order_by('-is_accepted', '-created_at')
    
    context = {
        'challenge': challenge,
        'solutions': solutions,
    }
    
    return render(request, 'qanda/challenge_detail.html', context)