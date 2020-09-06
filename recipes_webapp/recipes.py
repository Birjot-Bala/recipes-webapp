import requests

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session,
    current_app
)
from .oauth import get_token_from_cache
import msal

bp = Blueprint('recipes', __name__)

@bp.route('/')
def index():
    if not session.get("user"):
        return redirect(url_for("oauth.login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@bp.route("/form")
def form():
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))
    graph_data = requests.get(  # Use token to call downstream service
        current_app.config['ENDPOINT'],
        headers={'Authorization': 'Bearer ' + token['access_token']},
        params={'select':['id', 'name']},
        ).json()
    sections = {section["id"]:{"name":section["displayName"]} for section in graph_data["value"]}
    return render_template('form.html', sections=sections)

@bp.route("/search", methods=["POST"])
def search():
    token = get_token_from_cache(current_app.config['SCOPE'])
    if not token:
        return redirect(url_for("oauth.login"))
    if request.method == "POST":
        pages = []
        for section_id in request.form:
            _get_pages(
                form=request.form,
                url=f'https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages',
                token=token,
                pages=pages
            )
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

def _get_pages(form, url, token, pages=[]):
    # intial request
    pages_data = requests.get(
            url=url,
            headers={'Authorization': 'Bearer ' + token['access_token']},
            params={'select':['title', 'contentUrl']}
        ).json()
    for page in pages_data['value']:
        pages.append([page['title'], page['contentUrl']])
    if '@odata.nextLink' in pages_data: # recursion to collect all pages
        _get_pages(
            form=form, 
            url=pages_data['@odata.nextLink'], 
            token=token,
            pages=pages
        )

