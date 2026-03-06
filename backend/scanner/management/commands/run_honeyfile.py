from django.core.management.base import BaseCommand
from scanner.engines.honeyfile_monitor import HoneyfileMonitor
import os
import time

class Command(BaseCommand):
    help = 'Starts the ransomware honeyfile/decoy file monitor.'

    def handle(self, *args, **options):
        # We will create the decoy directory directly in the user's home/Documents 
        # folder to be realistic, or inside the project directory for testing.

        # For demonstration, let's put it in the user's home directory under 'Documents'
        home_dir = os.path.expanduser("~")
        watch_dir = os.path.join(home_dir, 'Documents', '_backup_decoys')
        
        # Alternatively, for safe testing without cluttering user files:
        # watch_dir = os.path.join(settings.BASE_DIR, 'temp_scans', '_decoys')

        self.stdout.write(self.style.SUCCESS(f'Initializing honeyfile trap in: {watch_dir}'))
        
        monitor = HoneyfileMonitor(watch_dir)
        monitor.start()
        
        self.stdout.write(self.style.SUCCESS('Monitor running. Listening for file modifications... (Press CTRL+C to quit)'))
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write('Stopping monitor...')
            monitor.stop()
            self.stdout.write('Done.')
