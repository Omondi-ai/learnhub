import random
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.learning.models import Cohort, Week, User, PeerPairing

class Command(BaseCommand):
    help = "Pair learners mutually for a given week."

    def add_arguments(self, parser):
        parser.add_argument('week_id', type=int, help='ID of the Week')

    @transaction.atomic
    def handle(self, *args, **options):
        week_id = options['week_id']
        try:
            week = Week.objects.get(id=week_id)
        except Week.DoesNotExist:
            self.stderr.write(f"No week with id {week_id}")
            return

        learners = list(User.objects.filter(cohort=week.cohort, role='learner'))
        if len(learners) < 2:
            self.stderr.write("Need at least 2 learners.")
            return

        PeerPairing.objects.filter(week=week).delete()

        random.shuffle(learners)
        pairs_created = 0
        for i in range(0, len(learners) - 1, 2):
            a = learners[i]
            b = learners[i + 1]
            PeerPairing.objects.create(week=week, learner_a=a, learner_b=b)
            pairs_created += 1

        if len(learners) % 2 == 1:
            self.stdout.write(self.style.WARNING(
                f"Odd number of learners ({len(learners)}). Last learner unpaired."
            ))

        self.stdout.write(self.style.SUCCESS(
            f"Created {pairs_created} pair(s) for Week {week.number}."
        ))