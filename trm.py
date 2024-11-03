import time
import os
import signal
import sys
import logging
from transmission_rpc import Client

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def initialize_client(transmission_host, transmission_port):
    while True:
        try:
            transmission_client = Client(host=transmission_host, port=transmission_port)
            logging.info(f"Connected to {transmission_host}:{transmission_port}")
            return transmission_client
        except Exception as e:
            logging.error(e)
            logging.info("Retrying in 15 seconds...")
            time.sleep(15)

def remove_finished_torrents(transmission_client):
    torrents = transmission_client.get_torrents()
    finished_torrents = [t for t in torrents if t.status in ['seeding', 'stopped'] and t.percent_done == 1.0]
    for torrent in finished_torrents:
        try:
            transmission_client.remove_torrent(torrent.id, delete_data=False)
            logging.info(f"Removed finished torrent: {torrent.name}")
        except Exception as e:
            logging.error(f"Error removing torrent {torrent.name}: {e}")

def signal_handler(sig, frame):
    logging.info("Received shutdown signal. Exiting...")
    sys.exit(0)

def main():
    transmission_host = os.environ.get('TRANSMISSION_HOST', "localhost")
    transmission_port = int(os.environ.get('TRANSMISSION_PORT', 9091))

    if not (0 < transmission_port < 65536):
        logging.error("Invalid TRANSMISSION_PORT. Exiting...")
        sys.exit(1)

    signal.signal(signal.SIGTERM, signal_handler)
    transmission_client = initialize_client(transmission_host, transmission_port)

    while True:
        remove_finished_torrents(transmission_client)
        time.sleep(900)

if __name__ == "__main__":
    main()
