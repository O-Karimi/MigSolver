from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            # Instantly log them in so they don't have to type their password again
            login(request, user)
            # Send them to the Q&A forum!
            return redirect('qanda:challenge_list')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'basics/register.html', {'form': form})