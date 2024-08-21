import logging
import json
import requests
from pwnagotchi.plugins import Plugin


class Example(Plugin):
    __author__ = 'evilsocket@gmail.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'An example plugin for pwnagotchi that sends a Discord webhook with a backup file.'

    def __init__(self):
        logging.debug("example plugin created")

    def on_webhook(self, path, request):
        if path == '/example/webhook':
            self.send_discord_webhook()
            return "Webhook sent successfully."
        else:
            return "Invalid path for the webhook."

    def send_discord_webhook(self):
        webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'

        # Read the Pwnagotchi backup file
        with open('/root/pwnagotchi-', 'r') as file:
            backup_data = file.read()

        # Prepare Discord webhook payload
        payload = {
            'content': 'Pwnagotchi Backup File',
            'username': 'Pwnagotchi',
            'file': ('pwnagotchi_backup.yml', backup_data)
        }

        # Send HTTP POST request to Discord webhook
        response = requests.post(webhook_url, files=payload)

        if response.status_code == 200:
            logging.info('Discord webhook sent successfully.')
        else:
            logging.error(f'Failed to send Discord webhook. Status code: {response.status_code}, Response: {response.text}')