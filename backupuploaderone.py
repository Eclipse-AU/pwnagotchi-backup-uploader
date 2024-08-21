import logging
import requests
import json
import os

import pwnagotchi
import pwnagotchi.ui.faces as faces
import pwnagotchi.plugins as plugins

class backupuploaderone(plugins.Plugin):
    __author__ = 'charagarlnad'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    __description__ = 'Sends Pwnagotchi status webhooks to Discord.'

    def on_loaded(self):
        logging.info('Backup Uploader plugin loaded.')

    def on_internet_available(self, agent):
        display = agent.view()
        last_session = agent.last_session

        if last_session.is_new() and last_session.handshakes > 0:
            logging.info('Detected a new session and internet connectivity!')

            # Path to the Pwnagotchi backup file
            backup_file = '/root/pwnagotchi-backup.tar.gz'

            logging.info('Uploading latest backup to discord...')
            display.set('status', 'Uploading latest backup to discord...')
            display.update(force=True)

            try:
                # Check if the backup file exists before trying to open it
                if os.path.exists(backup_file):
                    with open(backup_file, 'rb') as backup_file:
                        data = {
                            'content': 'Here is your backup archive.',
                            'file': ('pwnagotchi-backup.tar.gz', backup_file)
                        }

                        requests.post(self.options['webhook_url'], files={'file': ('pwnagotchi-backup.tar.gz', backup_file)}, data={'content': 'Latest Pwnagotchi Backup:'})

                        last_session.save_session_id()

                        logging.info('Uploading Plugin...')
                        display.set('status', 'Uploading Plugin...')
                        display.update(force=True)
                else:
                    logging.error(f'Backup file not found: {backup_file}')
            except Exception as e:
                logging.exception('An error occurred in the Backup Uploader plugin.')
                display.set('face', faces.BROKEN)
                display.set('status', 'An error occurred in the Backup Uploader plugin.')
                display.update(force=True)