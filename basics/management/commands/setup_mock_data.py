import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from basics.models import Category
from qanda.models import Challenge, Solution, Vote
from wiki.models import WikiArticle

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates a robust set of mock data for the MigSolver platform'

    def handle(self, *args, **kwargs):
        self.stdout.write("Erasing old test data...")
        Challenge.objects.all().delete()
        Category.objects.all().delete()
        WikiArticle.objects.all().delete()
        
        # We won't delete all users so you don't lose your superuser, but we'll clear our mock users
        User.objects.filter(username__in=['AlexExpat', 'MariaMigrant', 'AdminSarah']).delete()

        self.stdout.write("Creating Users...")
        user1 = User.objects.create_user(username='AlexExpat', password='testpassword123')
        user2 = User.objects.create_user(username='MariaMigrant', password='testpassword123')
        admin_user = User.objects.create_superuser(username='AdminSarah', email='admin@migsolver.com', password='testpassword123')

        self.stdout.write("Creating Categories...")
        categories_data = ['EU Blue Card', 'Housing & Anmeldung', 'Taxes & Freelancing', 'Healthcare']
        categories = {}
        for cat in categories_data:
            obj, created = Category.objects.get_or_create(name=cat, slug=slugify(cat))
            categories[cat] = obj

        self.stdout.write("Creating Wiki Articles...")
        wiki1 = WikiArticle.objects.create(
            title="The Ultimate Guide to the EU Blue Card",
            content="The EU Blue Card is a residence permit for academics from outside the EU who take up employment in an EU Member State. \n\nTo qualify, you need a university degree and a job offer meeting the minimum salary threshold. The process usually takes 4-6 weeks once all documents are submitted.",
            author=admin_user
        )
        wiki1.categories.add(categories['EU Blue Card'])

        wiki2 = WikiArticle.objects.create(
            title="How to navigate the 'Anmeldung' process",
            content="Anmeldung is the mandatory registration of your residential address. You must do this within 14 days of moving into a new apartment. \n\nYou will need your passport, your rental contract, and a Wohnungsgeberbestätigung (landlord confirmation).",
            author=admin_user
        )
        wiki2.categories.add(categories['Housing & Anmeldung'])

        self.stdout.write("Creating Q&A Challenges & Solutions...")
        
        # Challenge 1
        c1 = Challenge.objects.create(
            title="Can I freelance on a standard work visa?",
            body="I am currently employed full-time on a standard IT work visa, but I got an offer to do some weekend freelance consulting. Am I legally allowed to invoice for this?",
            author=user1,
            is_solved=True
        )
        c1.categories.add(categories['Taxes & Freelancing'], categories['EU Blue Card'])

        s1 = Solution.objects.create(
            body="Usually, no. Standard work visas are tied directly to your primary employer. You have to explicitly apply to the Ausländerbehörde (Immigration Office) to have a 'freelance permission' added to your permit.",
            author=user2,
            challenge=c1,
            is_accepted=True
        )
        Vote.objects.create(user=user1, solution=s1, value=1)
        Vote.objects.create(user=admin_user, solution=s1, value=1)

        # Challenge 2
        c2 = Challenge.objects.create(
            title="Landlord refusing to give Wohnungsgeberbestätigung",
            body="I just moved into a sublet, but the main tenant says they can't give me the document I need for my Anmeldung. What are my options here?",
            author=user2,
            is_solved=False
        )
        c2.categories.add(categories['Housing & Anmeldung'])

        s2 = Solution.objects.create(
            body="Huge red flag. If they won't give you the document, it usually means the landlord doesn't know they are subletting to you (which is illegal). You cannot register your address without it.",
            author=user1,
            challenge=c2,
            is_accepted=False
        )
        Vote.objects.create(user=admin_user, solution=s2, value=1)

        s3 = Solution.objects.create(
            body="As a temporary workaround, sometimes hostels or long-term Airbnb hosts will provide you with the document, but you need to ask them explicitly before booking.",
            author=admin_user,
            challenge=c2,
            is_accepted=False
        )
        Vote.objects.create(user=user1, solution=s3, value=-1) # Downvoted answer!

        self.stdout.write(self.style.SUCCESS('Successfully populated MigSolver with mock data!'))