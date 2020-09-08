import requests
import sqlite3

import msal
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
    current_app
)
from .oauth import get_token_from_cache
from .db import get_db

bp = Blueprint('recipes', __name__)

@bp.route('/')
def index():
    if not session.get("user"):
        return redirect(url_for("oauth.login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)


@bp.route('/update')
def update():
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))

    db = get_db()

    graph_data = requests.get(  # Use token to call downstream service
        current_app.config['ENDPOINT'],
        headers={'Authorization': 'Bearer ' + token['access_token']},
        params={'select':['id', 'name']},
        ).json()
    # insert sections into database
    sections = [(section["id"], section["displayName"]) for section in graph_data["value"]]
    db.execute('DELETE FROM sections')
    db.executemany(
        'INSERT INTO sections (section_id, title) VALUES (?, ?)', sections
    )
    # get all pages and store contentUrl
    pages = []
    for section in sections:
        _get_pages(
            section=section,
            url=f'https://graph.microsoft.com/v1.0/me/onenote/sections/{section[0]}/pages',
            token=token,
            pages=pages
        )
    db.execute('DELETE FROM pages')
    db.executemany(
        'INSERT INTO pages (section_id, title, contentUrl) VALUES (?, ?, ?)',
        pages
    )
    db.commit()
    return redirect(url_for('recipes.index'))

@bp.route("/form")
def form():
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))

    db = get_db()
    # select section ids and titles from db
    sections = db.execute('SELECT * FROM sections').fetchall()

    # graph_data = requests.get(  # Use token to call downstream service
    #     current_app.config['ENDPOINT'],
    #     headers={'Authorization': 'Bearer ' + token['access_token']},
    #     params={'select':['id', 'name']},
    #     ).json()
    # sections = {section["id"]:{"name":section["displayName"]} for section in graph_data["value"]}
    # return render_template('form.html', sections=sections)

    
    return render_template('form.html', sections=sections)


@bp.route("/search", methods=["POST"])
def search():
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))
    
    if request.method == "POST":
        db = get_db()
        pages = []
        for section_id in request.form:
            pages += db.execute('SELECT * FROM pages WHERE section_id=?', (section_id,)).fetchall()

    return render_template('pages.html', pages=pages)


@bp.route("/search/<page>")
def search_page(page):
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))
    contentUrl = request.args.get('contentUrl')
    recipe = requests.get(
        url=contentUrl,
        headers={'Authorization': 'Bearer ' + token['access_token']},
        )
    return render_template('test.html', title=page, content=recipe.text)


def _get_pages(section, url, token, pages=[]):
    # intial request
    pages_data = requests.get(
            url=url,
            headers={'Authorization': 'Bearer ' + token['access_token']},
            params={'select':['title', 'contentUrl']}
        ).json()
    for page in pages_data['value']:
        pages.append((section[0],) + (page['title'], page['contentUrl']))
    if '@odata.nextLink' in pages_data: # recursion to collect all pages
        _get_pages(
            section=section, 
            url=pages_data['@odata.nextLink'], 
            token=token,
            pages=pages
        )

