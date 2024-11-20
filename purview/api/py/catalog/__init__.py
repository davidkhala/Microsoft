from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient
import json
from catalog.entity import Entity
from catalog.relationship import Relationship


class Catalog:
    def __init__(self, **kwargs):
        credentials = DefaultAzureCredential()
        self.client = PurviewCatalogClient("https://api.purview-service.microsoft.com", credentials, **kwargs)

    def assets(self, search_request=None):
        if search_request is None:
            search_request = {"keywords": "*"}
        r = self.client.discovery.query(search_request)
        return r['value']

    def get_entity(self, type_name, qualified_name):
        r = self.client.entity.get_by_unique_attributes(type_name, attr_qualified_name=qualified_name)
        return Entity(r)

    def lineage_table(self, _entity: Entity, upstreams, downstreams):
        sources = [{'guid': id} for id in upstreams] if upstreams else []
        sinks = [{'guid': id} for id in downstreams] if downstreams else []
        r = self.client.entity.create_or_update({
            'entity': {
                'attributes': {
                    'qualifiedName': _entity.qualifiedName,
                    'name': _entity.name
                },
                'relationshipAttributes': {
                    'sources': sources,
                    'sinks': sinks
                },
                'guid': _entity.guid,
                'typeName': _entity.type
            }
        })
        if r.get('mutatedEntities'):
            return r['mutatedEntities']['UPDATE']
        else:
            return r['guidAssignments']

    def lineage_column(self, _relationship: Relationship, columns):
        column_mapping = json.dumps([
            {'Source': key, 'Sink': value or key} for key, value in columns.items()
        ])

        return self.client.relationship.update({
            'guid': _relationship.guid,
            'typeName': _relationship.typeName,
            'attributes': {
                'columnMapping': column_mapping,
            }
        })
