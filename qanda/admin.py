from django.contrib import admin
from .models import Challenge, Solution, Vote

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_solved')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('title', 'author__username')

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'author', 'created_at', 'is_accepted')
    list_filter = ('is_accepted',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'solution', 'value')