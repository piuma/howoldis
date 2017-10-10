import arrow
import wptools
import functools
from jinja2 import Markup

class Person:
    what = "human"
    name = None
    description = None
    extract = None
    wikidata = {}
    birth = None
    death = None
    is_death = True
    age = None
    pageid = None
    thumbnail = None
    pageimage = None
    lang = None
    
    def __init__(self, people):
        self.name = people['title']
        self.extract = Markup(people['extract'])
        try:
            self.thumbnail = people['thumbnail']
        except KeyError:
            pass
        
        try:
            self.pageimage = people['pageimage']
        except KeyError:
            pass

        self._retrive_info()

        
    @functools.lru_cache(maxsize=128, typed=False)
    def _retrive_info(self):
        page = wptools.page(self.name)
        wikidata = page.get_wikidata()
        self.birth = arrow.get(wikidata.wikidata['birth'])
        try:
            self.death = arrow.get(wikidata.wikidata['death'])
        except KeyError:
            self.death = arrow.now()
            self.is_death = False
        self.age = int((self.death - self.birth).days / 365)

        self.lang = wikidata.lang
        self.description = Markup(wikidata.description)
        
        # info = page.get_query()
        # thumbnail = info.images[i].url for i in info.images if info.images[i].kind == 'query-thumbnail'

        
