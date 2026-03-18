from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.text import slugify
from django.db.models.functions import Coalesce
from .models import Challenge, Solution, Vote
from .forms import ChallengeForm, SolutionForm
from basics.models import Category

def challenge_list(request):
    challenges = Challenge.objects.all().order_by('-created_at')
    context = {'challenges': challenges}
    return render(request, 'qanda/challenge_list.html', context)

def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    

    solutions = challenge.solutions.annotate(
        total_votes=Coalesce(Sum('votes__value'), 0)
    ).order_by('-is_accepted', '-total_votes', '-created_at')

    # Handle the Solution Form submission
    if request.method == 'POST':
        # If they aren't logged in, send them to the admin login page for now
        if not request.user.is_authenticated:
            return redirect('/admin/login/?next=' + request.path)
            
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False) # Pause before saving to database
            solution.author = request.user     # Attach the logged-in user
            solution.challenge = challenge     # Attach this specific question
            solution.save()                    # Now save it!
            return redirect('qanda:challenge_detail', challenge_id=challenge.id)
    else:
        form = SolutionForm()

    context = {
        'challenge': challenge,
        'solutions': solutions,
        'form': form,
    }
    return render(request, 'qanda/challenge_detail.html', context)

# NEW VIEW: Asking a Question
@login_required(login_url='/admin/login/')
def ask_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            challenge = form.save(commit=False)
            challenge.author = request.user
            challenge.save()
            form.save_m2m() # Required to save the Many-to-Many categories!
            return redirect('qanda:challenge_detail', challenge_id=challenge.id)
    else:
        form = ChallengeForm()
        
    return render(request, 'qanda/ask_challenge.html', {'form': form})

@login_required(login_url='/admin/login/')
def vote_solution(request, solution_id, value):
    # Security check: Ensure we only accept POST requests to change data
    value = int(value)  # Convert the string from the URL to an integer
    
    if request.method == 'POST':
        solution = get_object_or_404(Solution.objects.filter(id=solution_id))
        
        # Check if this user has already voted on this specific solution
        existing_vote = Vote.objects.filter(user=request.user, solution=solution).first()
        
        if existing_vote:
            if existing_vote.value == value:
                # Toggle off: If they clicked the same button again, delete their vote
                existing_vote.delete()
            else:
                # Change mind: If they went from +1 to -1 (or vice versa), update it
                existing_vote.value = value
                existing_vote.save()
        else:
            # Brand new vote
            Vote.objects.create(user=request.user, solution=solution, value=value)
            
    # Send them right back to the question page they were looking at
    return redirect(request.META.get('HTTP_REFERER', '/'))