from django.core.management.base import BaseCommand
from gunSounds.models import AudioClip

class Command(BaseCommand):
    help = 'Check what distances exist in the database'

    def handle(self, *args, **options):
        distances = AudioClip.objects.values_list('distance', flat=True).distinct().order_by('distance')
        self.stdout.write(f'Distinct distances in database: {list(distances)}')
        
        for distance in distances:
            count = AudioClip.objects.filter(distance=distance).count()
            self.stdout.write(f'  {distance}: {count} clips')
