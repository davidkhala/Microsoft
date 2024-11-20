import {DefaultAzureCredential} from "@azure/identity";
export class Abstract {
    constructor(credential = new DefaultAzureCredential()) {
        this.credential = credential;
        this.endpoint = 'https://api.purview-service.microsoft.com'
    }
}


