from json import JSONEncoder

class CardEntryEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class CardEntry: 
    position = -1
    title = None
    thumbnail = None
    slug_type = None

    def __init__(self, position, title, thumbnail):
        super().__init__()
        self.position = position
        self.title = title
        self.thumbnail = thumbnail

    def _makeSlug(self):   
        self.slug_type = title.split()
        for word in self.slug_type:
            self.slug_type += word.lower() + "-"
        
        self.slug_type = self.slug_type[0 : len(self.slug_type)-1]
        