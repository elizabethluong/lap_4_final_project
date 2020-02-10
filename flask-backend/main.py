import flask
from flask import Flask, redirect, url_for
from flask_dance.contrib.spotify import make_spotify_blueprint, spotify
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = flask.Flask("__main__")
app.config['SECRET_KEY'] = 'secretkey'

spotify_blueprint = make_spotify_blueprint(
    client_id='3d43242b1d914179a718dbf4c7125a0a', client_secret='2edec333089d49b98ba4589353f16243')

app.register_blueprint(spotify_blueprint, url_prefix='/spotify_login')


@app.route('/spotify')
def spotify_login():
    if not spotify.authorized:
        return redirect(url_for("spotify.login"))

    account_info = spotify.get('/v1/me')

    if account_info.ok:
        account_info_json = account_info.json()

        return '<h1>Hi your Spotify name is @{}'.format(account_info_json['display_name'])

    return '<h1>Request failed</h1>'


@app.route("/")
def my_index():
    return flask.render_template("index.html", token="Hello Flask + React")


app.run(debug=True)
