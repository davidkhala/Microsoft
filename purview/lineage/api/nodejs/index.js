import { axiosPromise } from "@davidkhala/axios";

export class API {
    constructor(accountname = "admin-david") {
        this.base_url = `https://${accountname}.purview.azure.com`;
    }

    async curl(opts, otherOptions) {
        if (!opts.url){
            opts.url = this.base_url + opts.route
        }
        return axiosPromise(opts, otherOptions)
    }

}