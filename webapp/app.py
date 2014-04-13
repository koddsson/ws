import requests

from flask import Flask, render_template

app = Flask(__name__)

app.config.update(
    DEBUG=True
)


@app.route("/")
def index():
    results = requests.get('http://localhost:3102/wallpaper/').json()
    wallpapers = []
    for filename in results:
        wallpapers.append(
            {'src': 'http://localhost:3102/wallpaper/{filename}'.format(
                filename=filename), 'sfw': True, 'tags': []})
    return render_template('index.html', untagged_wallpapers=wallpapers)

if __name__ == "__main__":
    app.run()
