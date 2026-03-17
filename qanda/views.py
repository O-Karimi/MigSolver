from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Challenge
from .forms import ChallengeForm, SolutionForm

def challenge_list(request):
    challenges = Challenge.objects.all().order_by('-created_at')
    context = {'challenges': challenges}
    return render(request, 'qanda/challenge_list.html', context)

def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
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