# Import flask and template operators
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_babel import Babel, gettext, ngettext
import functools
import wptools
import arrow
import json
from pprint import pprint

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

@functools.lru_cache(maxsize=128, typed=False)
def _search(name):
    if (name == "alfred einstain"):
        return _test_search(name)
    
    info = _get_info(name)
    return info, None

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

#@functools.lru_cache(maxsize=128, typed=False)
def _get_info(name):
    page = wptools.page(name)
    info = page.get_wikidata()
    # info = page.get_query()
    # thumbnail = info.images[i].url for i in info.images if info.images[i].kind == 'query-thumbnail'
    return info


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
        info, suggestions = _search(name)
    except LookupError:
        return render_template('result.html', name=name,
                               suggestions=suggestions)
    except Exception as e:
        print("error %s" % e)
        return render_template('error.html', name=name, message=e)

    if info.what != "human":
        return render_template('result.html',
                               age=gettext("Non e` una persona"),
                               info=info)

    info.death = True
    birth = arrow.get(info.wikidata['birth'])
    try:
        death = arrow.get(info.wikidata['death'])
    except KeyError:
        death = arrow.now()
        info.death = False
    age = int((death - birth).days / 365)
    return render_template('result.html', info=info, age=age, suggestions=suggestions)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
