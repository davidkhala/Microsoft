import {Abstract, getResponse} from "./interface.js";
import PurviewDataMap from "@azure-rest/purview-datamap"
import {Entity} from "./format/reduce.js";

// import {AtlasEntityWithExtInfo, PurviewDataMapClient, QueryOptions} from "@azure-rest/purview-datamap"

const {default: createClient} = PurviewDataMap

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

    async relationShow(guid) {
        const r = await this.client.path('atlas/v2/relationship/guid/{guid}', guid).get()
        return getResponse(r).relationship
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
        if (upstreams) {
            data.entity.relationshipAttributes.sources = upstreams.map(source => {
                const {guid} = source
                return {
                    guid
                }
            })
        }
        const r = await this.client.path("/atlas/v2/entity").post({body: data})
        const {guidAssignments, mutatedEntities} = getResponse(r)
        if (mutatedEntities) {
            return mutatedEntities.UPDATE
        } else return guidAssignments

    }

    async columnLineage(relationshipGuid, columns, typeName) {

        const columnMapping = JSON.stringify(Object.entries(columns).map(([key, value]) => ({
            Source: key,
            Sink: value
        })))
        if (!typeName) {
            const r = await this.relationShow(relationshipGuid)
            typeName = r.typeName
        }
        const r = await this.client.path('/atlas/v2/relationship').put({
            body: {
                guid: relationshipGuid,
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

    async entityGet(typeName, qualifiedName) {
        const r = await this.client.path('/atlas/v2/entity/uniqueAttribute/type/{typeName}', typeName).get({
            queryParameters: {
                'attr:qualifiedName': qualifiedName
            }
        })
        return new Entity(getResponse(r))

    }
}