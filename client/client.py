import os
import json
import socket
import websocket
import urllib
import subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import settings

import logging
logging.basicConfig(format="[%(levelname)s] %(message)s")

# Deal with this shit somehow
WALLPAPER_SERVER_PORT = 3101
#WALLPAPER_SERVER_HOST = 'koddsson.com'
WALLPAPER_SERVER_HOST = 'localhost'

WALLPAPER_DIR = 'wallpapers/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SETTINGS_FILE_PATH = (os.path.dirname(os.path.realpath(__file__)) +
                      '/settings.py')


class SettingsModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == SETTINGS_FILE_PATH:
            logger.info('Config file changed! Realoding!')
            reload(settings)
            send_config()


def set_wallpaper(filepath):
    # TODO: This currently only works on linux.
    subprocess.call(['feh', '--bg-fill', filepath])


def on_message(ws, message):
    logger.debug('Recieving {message}'.format(message=message))
    data = json.loads(message)
    if('wallpaper_url' in data):
        filename = data['wallpaper_url'].replace('wallpaper/', '')
        url = 'http://{server}:{port}/{url}'.format(
            port=WALLPAPER_SERVER_PORT + 1, server=WALLPAPER_SERVER_HOST,
            url=data['wallpaper_url'])
        logger.debug('Fetching wallpaper from {url}'.format(url=url))
        urllib.urlretrieve(url, WALLPAPER_DIR + filename)
        set_wallpaper(WALLPAPER_DIR + filename)


def on_error(ws, error):
    try:
        raise error
    except websocket.WebSocketConnectionClosedException:
        logger.error("Remote server closed the connection unexpectetly")
    except socket.error as error:
        if error.errno == 111:
            logger.error("Host is up but refusing connection. Is the service "
                         "running on the remote host?")
    except:
        raise error


def on_close(ws):
    logger.info("Quitting...")


def on_open(ws):
    logger.info('Connected!')
    send_config()


def send_config():
    # TODO: Get filters and send them.
    ws.send(json.dumps(
        {'filter': {'sfw': settings.sfw},
         'interval': settings.wallpaper_change_interval}))

if __name__ == "__main__":
    event_handler = SettingsModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    ws = websocket.WebSocketApp("ws://{host}:{port}/".format(
                                host=WALLPAPER_SERVER_HOST,
                                port=WALLPAPER_SERVER_PORT),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
