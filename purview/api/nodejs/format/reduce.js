export class Entity {
    /**
     *
     * @param {AtlasEntityWithExtInfoOutput} body
     */
    constructor(body) {
        this.body = body;
    }

    get entity() {
        return this.body.entity
    }

    get guid() {
        return this.entity.guid
    }

    get name() {
        return this.entity.attributes.name
    }

    get qualifiedName() {
        return this.entity.attributes.qualifiedName
    }

    get id() {
        return this.guid
    }

    get relationship() {
        return this.entity.relationshipAttributes
    }

    relationBySourceId(guid) {
        const found = this.relationship.sources.find(source => source.guid === guid)
        if (found) {
            const {relationshipGuid, relationshipType} = found
            return {guid: relationshipGuid, typeName: relationshipType}
        }
    }

    relationBySinkId(guid) {
        return this.relationship.sinks.find(sink => sink.guid === guid).relationshipGuid
    }

    /**
     * source relationship id list
     */
    get upstream_relations() {
        return this.relationship.sources.map(({relationshipGuid}) => relationshipGuid)
    }

    /**
     * sink relationship id list
     */
    get downstream_relations() {
        return this.relationship.sinks.map(({relationshipGuid}) => relationshipGuid)
    }

    get type() {
        return this.entity.typeName
    }

    get entityType() {
        return this.type
    }
}