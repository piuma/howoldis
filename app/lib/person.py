import arrow
import wptools
import functools

class Person:
    what = "human"
    name = None
    description = None
    wikidata = {}
    birth = None
    death = None
    is_death = True
    age = None
    pageid = None
    thumbnail = None
    pageimage = None
    
    def __init__(self, person):
        self.name = person.title
        self.extract = person.extract
        self.thumbnail = person.thumbnail
        self.pageimage = person.pageimage
        self._retrive_info()

        
    @functools.lru_cache(maxsize=128, typed=False)
    def _retrive_info(self):
        page = wptools.page(name)
        wikidata = page.get_wikidata()
        self.birth = wikidata['birth']
        try:
            self.death = arrow.get(wikidata['death'])
        except KeyError:
            self.death = arrow.now()
            self.is_death = False
        self.age = self.age = int((death - birth).days / 365)
        
        # info = page.get_query()
        # thumbnail = info.images[i].url for i in info.images if info.images[i].kind == 'query-thumbnail'

        
