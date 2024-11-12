import {PurviewAccountClient} from "@azure-rest/purview-administration";
import {PurviewManagementClient} from '@azure/arm-purview';
import {Abstract} from "./interface.js";

export class Account extends Abstract {


    async defaultAccount(tenantID, subscriptionId) {
        const client = new PurviewManagementClient(this.credential, subscriptionId);
        const {accountName, resourceGroupName} = await client.defaultAccounts.get(tenantID, "Tenant")
        this.accountName = accountName
        return {accountName, resourceGroupName}

    }

    set accountName(accountName) {
        super.accountName = accountName
        this.client = PurviewAccountClient(this.endpoint, this.credential);
    }

    async collections(){
        const {body}= await this.client.path("/collections").get()
        return body
    }

}
