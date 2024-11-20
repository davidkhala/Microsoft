import {Abstract} from "./interface.js";
import PurviewDataMap, {isUnexpected} from "@azure-rest/purview-datamap"
import {Entity} from "./format/reduce.js";

// import {AtlasEntityWithExtInfo, PurviewDataMapClient, QueryOptions} from "@azure-rest/purview-datamap"

const {default: createClient} = PurviewDataMap

export const getResponse = (r) => {
    if (isUnexpected(r)) {
        throw r;
    }
    return r.body
}

export class DataMap extends Abstract {
    constructor(credential) {
        super(credential);
        /**
         * @type PurviewDataMapClient
         */
        this.client = createClient(this.endpoint, this.credential);
    }

    async types() {
        // https://learn.microsoft.com/en-us/rest/api/purview/datamapdataplane/type/list?view=rest-purview-datamapdataplane-2023-09-01&tabs=HTTP
        const result = await this.client.path("/atlas/v2/types/typedefs").get({
            queryParameters: {includeTermTemplate: true}
        });

        return getResponse(result)
    }

    async entityTypes() {
        const {entityDefs} = await this.types()
        return entityDefs.map(e => e.name);
    }

    /**
     *
     * @return {Promise<AtlasRelationshipOutput>}
     */
    async relationShow(guid) {
        const r = await this.client.path('atlas/v2/relationship/guid/{guid}', guid).get()
        return getResponse(r).relationship
    }

    /**
     *
     * @param guid The globally unique identifier of the entity.
     * @returns {Promise<*>}
     */
    async lineageGet(guid) {
        const r = await this.client.path("/atlas/v2/lineage/{guid}", guid).get()
        return getResponse(r)
    }

    async lineageCreate({upstreams, downstreams, qualifiedName, name, guid, entityType}) {

        /**
         * @type AtlasEntityWithExtInfo
         */
        const data = {
            entity: {
                attributes: {
                    qualifiedName, name
                },
                relationshipAttributes: {
                    sources: upstreams ? upstreams.map(id => ({guid: id})) : [],
                    sinks: downstreams ? downstreams.map(id => ({guid: id})) : []
                },
                guid,
                typeName: entityType
            }

        }
        const r = await this.client.path("/atlas/v2/entity").post({body: data})
        const {guidAssignments, mutatedEntities} = getResponse(r)
        if (mutatedEntities) {
            return mutatedEntities.UPDATE
        } else return guidAssignments

    }

    /**
     *
     * @param guid
     * @param typeName
     * @param {Record<string, string>} columns map with key for source column, value for sink column
     */
    async columnLineage({guid, typeName}, columns) {

        const columnMapping = JSON.stringify(Object.entries(columns).map(([key, value]) => ({
            Source: key,
            Sink: value || key
        })))
        if (!typeName) {
            const r = await this.relationShow(guid)
            typeName = r.typeName
        }
        const r = await this.client.path('/atlas/v2/relationship').put({
            body: {
                guid,
                typeName,
                attributes: {
                    columnMapping,
                }
            }
        })
        return getResponse(r)

    }

    /**
     *
     * @param {QueryOptions} opts
     * @returns {Promise<*>}
     */
    async assets(opts = {
        keywords: "*"
    }) {
        const r = await this.client.path("/search/query").post({body: opts})
        return getResponse(r).value
    }


    async entityShow(guid) {
        const r = await this.client.path(`/atlas/v2/entity/guid/{guid}`, guid).get()

        return new Entity(getResponse(r))
    }

    async entityDelete(guid, throwIfNotFound) {
        try {
            await this.entityShow(guid)
        } catch (e) {
            if (e.status === '404' && !throwIfNotFound) {
                return false
            }
            throw e
        }
        getResponse(await this.client.path(`/atlas/v2/entity/guid/{guid}`, guid).delete())
        return true
    }

    /**
     *
     * @return {Promise<Entity>}
     */
    async entityGet(typeName, qualifiedName) {
        const r = await this.client.path('/atlas/v2/entity/uniqueAttribute/type/{typeName}', typeName).get({
            queryParameters: {
                'attr:qualifiedName': qualifiedName
            }
        })
        return new Entity(getResponse(r))

    }
}