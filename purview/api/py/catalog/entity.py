from catalog.relationship import Relationship


class Entity:
    def __init__(self, body: dict):
        self.entity = body['entity']
        self.referredEntities = body['referredEntities']

    @property
    def guid(self):
        return self.entity['guid']

    @property
    def name(self):
        return self.entity['attributes']['name']

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
