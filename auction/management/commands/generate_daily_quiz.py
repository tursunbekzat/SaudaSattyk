from django.core.management.base import BaseCommand
from django.utils import timezone
from auction.models import Quiz
from auction.quiz_generator import generate_quiz

class Command(BaseCommand):
    help = 'Generates the daily quiz'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        if not Quiz.objects.filter(date=today).exists():
            questions = generate_quiz()
            Quiz.objects.create(date=today, questions=questions)
            self.stdout.write(self.style.SUCCESS('Successfully generated quiz for today'))
