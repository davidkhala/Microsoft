import {DefaultAzureCredential} from "@azure/identity";
import {isUnexpected} from "@azure-rest/purview-datamap";

export class Abstract {
    constructor(credential = new DefaultAzureCredential()) {
        this.credential = credential;
    }

    set accountName(accountName) {
        this.endpoint = 'https://api.purview-service.microsoft.com'
    }
}

export const getResponse = (r) => {
    if (isUnexpected(r)) {
        throw r;
    }
    return r.body
}

