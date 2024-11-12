import { axiosPromise } from "@davidkhala/axios";
export class Lineage {
    async create(opts) {
        // POST https://{accountname}.purview.azure.com/datamap/api/atlas/v2/entity/bulk?api-version=2023-09-01
        return axiosPromise({
            url: `${this.base_url}/datamap/api/atlas/v2/entity/bulk?api-version=2023-09-01`,
            method: 'POST',
            ...opts
        })
    }
}