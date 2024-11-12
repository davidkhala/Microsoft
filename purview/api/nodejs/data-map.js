import {Abstract, getResponse} from "./interface.js";
import PurviewDataMap from "@azure-rest/purview-datamap"

// import {AtlasEntity, AtlasEntityWithExtInfo, PurviewDataMapClient} from "@azure-rest/purview-datamap/types/purview-datamap"
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

    /**
     *
     * @param {AtlasEntity} entity
     */
    async updateLineage(entity) {

        /**
         * @type AtlasEntityWithExtInfo
         */
        const data = {
            entity
        }
        const r = await this.client.path("/atlas/v2/entity").post({body: data})
        return getResponse(r)
    }

    async entityList(typeName) {
        const r = await this.client.path(`/atlas/v2/entity/bulk/uniqueAttribute/type/${typeName}`).get()
        return getResponse(r)
    }
}