# Import flask and template operators
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_babel import Babel, gettext, ngettext, format_date
import functools
import json
from pprint import pprint
import traceback
import requests
from lib.person import Person
from lib.search import wikisearch

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_pyfile('../config.py', silent=True)

babel = Babel(app)

@babel.localeselector
def get_locale():
    """ automatically choose the best matching locale,
    based on the Accept-Language header from the incoming request. """
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

def first(s):
    '''Return the first element from an ordered collection
       or an arbitrary element from an unordered collection.
       Raise StopIteration if the collection is empty.
    '''
    return next(iter(s))


@app.template_filter('formatdate')
def formatdate(d):
    return format_date(d.date())


def _test_search(name):
    with open("/home/mazzetta/prog/howoldis/alfred_einstain.json") as json_data:
        suggestions = json.load(json_data)
    #pprint(suggestions)
    
    pprint(suggestions[0])

    class person:
        what = "human"
        name = "Alfred Einstain"
        label = "Alfred Einstain"
        description = """<p><b>Alfred Einstein</b>
(December 30, 1880\u00a0\u2013 February 13, 1952) was a German-American
musicologist and music editor.</p>"""
        wikidata = {}
        def __init__(self):
            self.wikidata['birth'] = "2015-01-12 12:23:00,0"
        
        
    info = person()
    #info = _get_info(results[0][1]['title'])

    return info, suggestions[1:5]

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', "", type=str)
    
    #return jsonify(matching_results=results)
    return """{
    "query": "Unit",
    "suggestions": ["United Arab Emirates", "United Kingdom", "United States"] } """


@app.route('/')
@app.route('/<string:name>')
def index(name=None):
    name = request.args.get('name', name)

    if name is None:
        return render_template('result.html')
    
    try:
        friends = wikisearch(name)
    except LookupError:
        tb = traceback.format_exc()
        print(tb)
        return render_template('result.html', name=name)
    except requests.exceptions.ConnectionError as e:
        return render_template('error.html', name=name, message="Connection error")
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return render_template('error.html', name=name, message=e)

    
    try:
        print("=" * 20)
        pprint(friends[0][1])
        person = Person(friends[0][1])
        friends = friends[1:5]
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return render_template('error.html', name=name, message=e)
    
    return render_template('result.html', person=person, friends=friends)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
