import os
import re
from django.core.management.base import BaseCommand
from gunSounds.models import Gun, AudioClip
from google.cloud import storage

class Command(BaseCommand):
    help = 'Populate database from GCP bucket'

    def handle(self, *args, **options):
        project_id = 'portfoliosite-468605'
        bucket_name = 'portfoliosite-media-files'
        # Map numeric distances to model distances
        distance_mapping = {
            '100': '100m',
            '200': '200m',
            '300': '320m',  # 300 yards ≈ 320m
            '320': '320m',
            '400': '400m',
            '490': '490m',
            '500': '490m',  # 500 yards ≈ 490m
        }
        
        # Clear all existing data to start fresh
        self.stdout.write(self.style.WARNING('Clearing existing Gun and AudioClip data...'))
        AudioClip.objects.all().delete()
        Gun.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared all existing data'))
        
        try:
            client = storage.Client(project=project_id)
            bucket = client.bucket(bucket_name)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to GCS: {e}'))
            return

        audio_files = [blob.name for blob in bucket.list_blobs(prefix='audio/') 
                      if blob.name.endswith(('.wav', '.mp3', '.ogg', '.flac'))]
        self.stdout.write(f'Found {len(audio_files)} audio files')
        
        created_count = 0
        updated_count = 0
        
        for audio_path in audio_files:
            filename = os.path.basename(audio_path)
            filename_no_ext = os.path.splitext(filename)[0]
            match = re.match(r'^(.+?)_(\d+)$', filename_no_ext)
            
            if not match:
                self.stdout.write(self.style.WARNING(f'Could not parse: {filename}'))
                continue
            
            weapon_name = match.group(1)
            distance_num = match.group(2)
            
            # Map distance using the mapping dictionary
            found_distance = distance_mapping.get(distance_num)
            if not found_distance:
                self.stdout.write(self.style.WARNING(f'No distance mapping for {distance_num}m in {filename}'))
                continue
            
            try:
                gun, gun_created = Gun.objects.get_or_create(
                    name=weapon_name,
                    defaults={'ammo_type': 'Unknown', 'size': 'Unknown'}
                )
                
                clip, clip_created = AudioClip.objects.get_or_create(
                    gun=gun, 
                    label=f'{weapon_name} at {found_distance}',
                    distance=found_distance,
                    defaults={'audio_file': audio_path}
                )
                
                if clip_created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {weapon_name} - {found_distance}'))
                else:
                    # Update audio file if it changed
                    if clip.audio_file != audio_path:
                        clip.audio_file = audio_path
                        clip.save()
                        updated_count += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {filename}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'Done! Created: {created_count}, Updated: {updated_count}'))
