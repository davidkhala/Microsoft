from abc import abstractmethod

from davidkhala.purview.relationship import Relationship


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
        self.value = value

    def __str__(self):
        return self.value

    @property
    def score(self):
        return self.value["@search.score"]

    @property
    def assetType(self):
        return self.value['assetType'][0]

    @property
    def collectionId(self):
        return self.value['collectionId']

    @property
    def domainId(self):
        return self.value['domainId']

    @property
    def name(self):
        return self.value['name']

    @property
    def id(self):
        return self.value['id']

    @property
    def qualifiedName(self):
        return self.value['qualifiedName']

    @property
    def entityType(self):
        return self.value['entityType']

    @name.setter
    def name(self, value):
        self.value['name'] = value

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
