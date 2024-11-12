import assert from 'assert'
import {Account} from '../account.js'
import {DataMap} from "../data-map.js";
import {typeName} from '../interface.js'
import {type} from "mocha/lib/utils.js";

const tenantID = "c2a38aca-e9c7-4647-8dcd-9185476159ae"
const subscription = "d02180af-0630-4747-ab1b-0d3b3c12dafb"
const defaultAccountName = "admin-david"
describe('account', function () {
    this.timeout(0)
    it('default account', async () => {

        const account = new Account()
        const {accountName} = await account.defaultAccount(tenantID, subscription)
        assert.equal(accountName, defaultAccountName)

        const {body} = await account.client.path("/collections").get()
        console.debug(body)

    })
})
describe('data map', function () {
    this.timeout(0)
    const dataMap = new DataMap("admin-david")
    it('types', async () => {
        const result = await dataMap.types()
        console.debug(result.enumDefs)
    })
    it('entityTypes', async () => {
        const types = await dataMap.entityTypes()
        console.debug(types.filter(type=> type.includes('azure_sql_server')))
        console.debug(types.filter(type => type.includes('power')))
        console.debug(types.filter(type=> type.includes('databricks')))
    })
    it('update', async () => {
        const r = await dataMap.updateLineage({
            guid: "abc",
            typeName: "powerbi_dataset"
        })
        console.debug(r)
    })
    it('entity list', async () => {
        const r = await dataMap.entityList('azure_sql_server');
        console.debug(r)
    })
})