import {DefaultAzureCredential} from "@azure/identity";
import {isUnexpected} from "@azure-rest/purview-datamap";
import fs from 'fs'
export class Abstract {
    constructor(credential = new DefaultAzureCredential()) {
        this.credential = credential;
    }

    set accountName(accountName) {
        // this.endpoint = `https://${accountName}.purview.azure.com`;
        this.endpoint= 'https://api.purview-service.microsoft.com'
    }
}

export const getResponse = (r) => {
    if (isUnexpected(r)) {
        throw r;
    }
    return r.body
}

export const typeName = {
    powerbi: {
        dataset: "powerbi_dataset",
        report: 'powerbi_report'
    }
}
export const objectType = {
    table: "Tables"
}
