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
    async defaultAccount(tenantId){
        await axiosPromise({
            url: "https://management.azure.com/providers/Microsoft.Purview/getDefaultAccount",
            params: {
                scopeType: "Tenant",
                "api-version":"2021-12-01",
                scopeTenantId: tenantId
            }
        })

    }

}