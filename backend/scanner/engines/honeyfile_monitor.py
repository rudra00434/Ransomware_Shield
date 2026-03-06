import os
import time
import json
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

# List of files we will create as bait
DECOY_FILES = [
    'passwords.txt',
    'tax_returns_2025.pdf',
    'bitcoin_wallet.dat',
    'finance_q4.xlsx',
]

class HoneyfileEventHandler(FileSystemEventHandler):
    """
    Handles events when the watchdog observer detects file system changes.
    """
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.decoy_paths = [os.path.join(watch_dir, f) for f in DECOY_FILES]

    def _trigger_alert(self, event_type, file_path):
        """Send a critical alert through WebSockets."""
        logger.warning(f"RANSOMWARE TRAP TRIPPED: {event_type} on {file_path}")
        
        channel_layer = get_channel_layer()
        if channel_layer:
            alert_message = {
                'type': 'RANSOMWARE_HONEYPOT_ALERT',
                'severity': 'CRITICAL',
                'title': 'Ransomware Activity Detected!',
                'description': f"A critical decoy file ({os.path.basename(file_path)}) was just {event_type}. This is highly indicative of active ransomware encrypting your files.",
                'filepath': file_path,
                'event': event_type
            }
            
            # Broadcast to all connected clients listening to alerts
            # We use 'user_alerts_guest' as the default group from consumers.py
            async_to_sync(channel_layer.group_send)(
                'user_alerts_guest',
                {
                    'type': 'send_alert',
                    'message': alert_message
                }
            )

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.decoy_paths:
            self._trigger_alert('modified', event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path in self.decoy_paths:
            self._trigger_alert('deleted', event.src_path)

    def on_moved(self, event):
        if not event.is_directory and event.src_path in self.decoy_paths:
            self._trigger_alert('moved', event.src_path)


class HoneyfileMonitor:
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir
        self.observer = Observer()
        self.event_handler = HoneyfileEventHandler(self.watch_dir)

    def setup_decoys(self):
        """Create the decoy folder and the enticing files inside it."""
        if not os.path.exists(self.watch_dir):
            os.makedirs(self.watch_dir)
            logger.info(f"Created honeyfile directory at {self.watch_dir}")

        for filename in DECOY_FILES:
            filepath = os.path.join(self.watch_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as f:
                    f.write("CONFIDENTIAL INFORMATION. DO NOT DISTRIBUTE.\n")

        # Attempt to hide the directory on Windows
        if os.name == 'nt':
            import ctypes
            FILE_ATTRIBUTE_HIDDEN = 0x02
            ctypes.windll.kernel32.SetFileAttributesW(self.watch_dir, FILE_ATTRIBUTE_HIDDEN)

    def start(self):
        """Start the watchdog observer."""
        self.setup_decoys()
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=False)
        self.observer.start()
        logger.info(f"Honeyfile monitor started on {self.watch_dir}")

    def stop(self):
        """Stop the watchdog observer."""
        self.observer.stop()
        self.observer.join()
        logger.info("Honeyfile monitor stopped.")
