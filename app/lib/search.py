import arrow
import wikipedia
import functools
#from app.main import get_locale
from pprint import pprint

@functools.lru_cache(maxsize=128, typed=False)
def wikisearch(query, results=5, suggestion=False):
    '''
    Do a Wikipedia search for `query`.

    Keyword arguments:

    * results - the maxmimum number of results returned
    * suggestion - if True, return results and suggestion (if any) in a tuple
    '''
    """
    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'gsrsearch': 'hastemplate=Birth_date',
        'srsearch': query
    }
    """

    search_params = {
        "action": "query",
	"format": "json",
	"prop": "extracts",
	"continue": "",
	"generator": "search",
	"pithumbsize": "100",
	"pilimit": "max",
	"exsentences": "1",
        "exlimit": "max",
        "exintro": 1,
	"gsrsearch": "hastemplate:Birth_date %s" % query,
	"gsrnamespace": "0",
	"gsrlimit": results
    }
    
    if suggestion:
        search_params['srinfo'] = 'suggestion'


#    wikipedia.wikipedia.set_lang('en')
    raw_results = wikipedia.wikipedia._wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise HTTPTimeoutError(query)
        else:
            raise WikipediaException(raw_results['error']['info'])

    if not 'query' in raw_results:
        raise Exception("No 'query' in raw_results")
        
    sorted_results = sorted(raw_results['query']['pages'].items(), key=lambda x: x[1]['index'])
        
    pprint(raw_results)
    pprint(sorted_results)
    # print(json.dumps(sorted_results))
    return sorted_results


# mysearch("Barack")


"""
PREFIX wdno: <http://www.wikidata.org/prop/novalue/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

#Humans without children
SELECT ?human ?date_of_birth ?place_of_birthLabel ?date_of_death ?place_of_death ?place_of_deathLabel ?image WHERE {
  ?human wdt:P31 wd:Q5.
  ?human p:P40 ?childStatement.
  ?human wdt:P569 ?date_of_birth.
  ?childStatement rdf:type wdno:P40.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?human wdt:P19 ?place_of_birth. }
  OPTIONAL { ?human wdt:P570 ?date_of_death. }
  OPTIONAL { ?human wdt:P20 ?place_of_death. }
  OPTIONAL { ?human wdt:P18 ?image. }
}
LIMIT 20
"""
