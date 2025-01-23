from abc import abstractmethod

from davidkhala.microsoft.purview.relationship import Relationship


class AbstractEntity(dict):
    @property
    @abstractmethod
    def entityType(self):
        pass

    @property
    @abstractmethod
    def qualifiedName(self):
        pass

    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass


class Asset(AbstractEntity):
    def __init__(self, value: dict):
        super().__init__(value)

    @property
    def score(self):
        return self["@search.score"]

    @property
    def assetType(self):
        return self['assetType'][0]

    @property
    def collectionId(self):
        return self['collectionId']

    @property
    def domainId(self):
        return self['domainId']

    @property
    def name(self):
        return self['name']

    @property
    def id(self):
        return self['id']

    @property
    def qualifiedName(self):
        return self['qualifiedName']

    @property
    def entityType(self):
        return self['entityType']

    @name.setter
    def name(self, value):
        self['name'] = value


class Entity(AbstractEntity):
    def __init__(self, body: dict):
        super().__init__(body)
        self.entity = body['entity']
        self.referredEntities = body['referredEntities']

    @property
    def guid(self):
        return self.entity['guid']

    @property
    def name(self):
        return self.entity['attributes']['name']

    @name.setter
    def name(self, value):
        self.entity['attributes']['name'] = value

    @property
    def qualifiedName(self):
        return self.entity['attributes']['qualifiedName']

    @property
    def id(self):
        return self.guid

    @property
    def relationship(self):
        return self.entity['relationshipAttributes']

    @property
    def columns(self):
        return self.relationship['columns']

    @property
    def column_names(self):
        return list(map(lambda column: column['displayText'], self.columns))

    def relation_by_source_id(self, guid):
        found = next((source for source in self.relationship['sources'] if source['guid'] == guid), None)
        if found:
            return Relationship(found.get('relationshipGuid'), found.get('relationshipType'))

    def relation_by_sink_id(self, guid):
        found = next((sink for sink in self.relationship['sinks'] if sink['guid'] == guid), None)
        if found:
            return Relationship(found.get('relationshipGuid'), found.get('relationshipType'))

    @property
    def upstream_relations(self):
        return [source['relationshipGuid'] for source in self.relationship['sources']]

    @property
    def downstream_relations(self):
        return [sink['relationshipGuid'] for sink in self.relationship['sinks']]

    @property
    def type(self):
        return self.entity['typeName']

    @property
    def entityType(self):
        return self.type
