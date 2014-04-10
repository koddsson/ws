import json
import websocket
import urllib
import subprocess


WALLPAPER_SERVER_PORT = 1337
WALLPAPER_SERVER_HOST = 'localhost'

WALLPAPER_DIR = 'wallpapers/'


def set_wallpaper(filepath):
    # TODO: This currently only works on linux.
    subprocess.call(['feh', '--bg-fill', filepath])


def on_message(ws, message):
    print message
    data = json.loads(message)
    if('wallpaper_url' in data):
        filename = data['wallpaper_url'].replace('wallpaper/', '')
        url = 'http://{server}:{port}/{url}'.format(
            server=WALLPAPER_SERVER_HOST, port=WALLPAPER_SERVER_PORT,
            url=data['wallpaper_url'])
        urllib.urlretrieve(url, WALLPAPER_DIR + filename)
        set_wallpaper(WALLPAPER_DIR + filename)


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    ws.send(json.dumps({'request': 'wallpaper', 'filter': {}}))


if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:3000/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()
