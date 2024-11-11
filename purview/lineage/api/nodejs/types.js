import {API} from "./index.js";

// https://learn.microsoft.com/en-us/rest/api/purview/datamapdataplane/type/list?view=rest-purview-datamapdataplane-2023-09-01&tabs=HTTP
export class Types extends API {
    async list() {
        await this.curl({
            route: `/datamap/api/atlas/v2/types/typedefs?api-version=2023-09-01&includeTermTemplate=True`,

        })
    }
}