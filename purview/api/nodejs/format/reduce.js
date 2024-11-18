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

    get type() {
        return this.entity.typeName
    }

    get entityType() {
        return this.type
    }
}