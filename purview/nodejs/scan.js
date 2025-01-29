import PurviewScanning, {paginate} from "@azure-rest/purview-scanning";
import {Abstract} from "./interface.js";


const {default: createClient} = PurviewScanning

export default class Scan extends Abstract {
    constructor() {
        super();
        /**
         * @type PurviewScanningRestClient
         */
        this.client = createClient(this.endpoint, this.credential);
    }

    async sources() {
        const dataSources = await this.client.path("/scan/datasources").get();

        const items = [];
        const iter = paginate(this.client, dataSources)

        for await (const item of iter) {
            items.push(item);
        }
        return items
    }
}

