import re

class BaseModel:

    def parse(self, json):
        for key, value in json.items():
            key = self.camel_to_snake_case(key)
            lower_key = ''.join(e.lower() for e in key if e.isalnum())
            lower_attrs = { k.replace('_', '').lower() : k for k in self.__dict__.keys() }

            if lower_key in lower_attrs.keys():
                key = lower_attrs[lower_key]
                attr_value = getattr(self, key)

                if isinstance(attr_value, BaseModel):
                    setattr(self, key, attr_value.parse(value))
                else:
                    setattr(self, key, value)

        return self
    
    def get_json(self):

        dikt = {}
        for k, v in self.__dict__.items():
            if v:
                if isinstance(v, BaseModel):
                    json = v.get_json()
                    if json: dikt[k] = json
                else:
                    dikt[k] = v

        return dikt if len(dikt) > 0 else None
    
    @staticmethod
    def camel_to_snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
class ObjectListModel(BaseModel):

    list_object = None

    def __init__(self):
        self.list = []

    def __iter__(self):
        return iter(self.list)
    
    def add(self, item):
        self.list.append(item)
        return self.list
    
    def remove(self, item):
        self.list.remove(item)
        return self.list
    
    def parse(self, json):

        if isinstance(json, dict):
            item = self.list_object().parse(json)
            self.add(item)
        elif isinstance(json, list):
            for item in json:
                item = self.list_object().parse(item)
                self.add(item)

        return self
    
    def get_json(self):
        list = []

        for item in self.list:
            list.append(item.get_json())
        
        return list

class Error(BaseModel):
    
    def __init__(
        self,
        message=None
    ):
        
        self.message = message

class Errors(ObjectListModel):
    list_object = Error