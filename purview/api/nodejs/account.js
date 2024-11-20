import {PurviewAccountClient} from "@azure-rest/purview-administration";
import {PurviewManagementClient} from '@azure/arm-purview';
import {Abstract} from "./interface.js";

export function getResponse(response) {
    const {status, body} = response
    if (status === '200') {
        return body
    } else {
        throw response
    }
}


export class Account extends Abstract {


    constructor() {
        super();
        this.client = PurviewAccountClient(this.endpoint, this.credential);
    }

    async defaultAccount(tenantID, subscriptionId) {
        const client = new PurviewManagementClient(this.credential, subscriptionId);
        const {accountName, resourceGroupName} = await client.defaultAccounts.get(tenantID, "Tenant")
        this.accountName = accountName
        return {accountName, resourceGroupName}

    }

    async collections() {
        const r = await this.client.path("/collections").get()
        return getResponse(r)
    }

}
