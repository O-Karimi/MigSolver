from django.db import models
from django.conf import settings
from django.db.models import Sum
from basics.models import Category

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)
    
    # Links to the custom user model we built in the 'basics' app
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='challenges'
    )
    
    # This single line magically creates the ChallengeCategory Junction Table!
    categories = models.ManyToManyField(Category, related_name='challenges')

    def __str__(self):
        return self.title

class Solution(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solutions')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solutions')

    class Meta:
        ordering = ['-is_accepted', '-created_at']  # New: Sort solutions by newest first

    def __str__(self):
        return f"Solution by {self.author} on {self.challenge.title}"
    
class Vote(models.Model):
    value = models.SmallIntegerField(help_text="+1 for upvote, -1 for downvote")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='votes'
    )
    solution = models.ForeignKey(
        Solution, 
        on_delete=models.CASCADE, 
        related_name='votes'
    )

    class Meta:
        # This acts as your database constraint: one user gets exactly one vote per solution.
        unique_together = ('user', 'solution')

    def __str__(self):
        return f"{self.value} vote by {self.user} on Solution {self.solution.id}"