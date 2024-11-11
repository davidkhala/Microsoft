// POST https://{accountname}.purview.azure.com/datamap/api/atlas/v2/entity/bulk?api-version=2023-09-01

import {axiosPromise} from "@davidkhala/axios";

export class API {
    constructor(accountname="admin-david") {
        this.base_url = `https://${accountname}.purview.azure.com`;
    }

    async curl(opts, otherOptions) {
        opts.url = this.base_url + opts.route
        return axiosPromise(opts, otherOptions)
    }

}