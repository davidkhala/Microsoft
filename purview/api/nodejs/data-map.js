import {Abstract, getResponse} from "./interface.js";
import PurviewDataMap from "@azure-rest/purview-datamap"

// import {AtlasEntityWithExtInfo, PurviewDataMapClient, QueryOptions} from "@azure-rest/purview-datamap"

const {default: createClient} = PurviewDataMap

export class DataMap extends Abstract {
    constructor(accountName, credential) {
        super(credential);
        this.accountName = accountName
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
        return getResponse(r)
    }

    async lineageCreate({upstreams, downstreams, qualifiedName, name, id, entityType}) {

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
                guid: id,
                typeName: entityType
            }

        }
        if (upstreams) {
            const sources = upstreams.map(source => {
                const {guid, columns} = source

                const result = {
                    guid
                }
                // TODO Don't Work
                // if (columns) {
                //     const columnMapping = JSON.stringify(Object.entries(columns).map(([key, value]) => ({
                //         Source: key,
                //         Sink: value
                //     })))
                //     result.relationshipAttributes = {
                //         attributes: {
                //             columnMapping
                //         }
                //     }
                // }

                return result
            })
            console.debug('sources', sources)
            data.entity.relationshipAttributes.sources = sources
        }
        const r = await this.client.path("/atlas/v2/entity").post({body: data})

        return getResponse(r)
    }

    // TODO Don't Work
    async columnLineage(relationshipGuid, columns) {

        const columnMapping = JSON.stringify(Object.entries(columns).map(([key, value]) => ({
            Source: key,
            Sink: value
        })))

        const r= await this.client.path('/atlas/v2/relationship').put({
            body: {
                guid: relationshipGuid,
                attributes: {
                    columnMapping
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

        return getResponse(r)
    }
}