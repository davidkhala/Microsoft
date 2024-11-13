import assert from 'assert'
import {Account} from '../account.js'
import {DataMap} from "../data-map.js";
import {JSONReadable} from '@davidkhala/light/format.js'
import fs from 'fs'

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
        console.debug(types.filter(type => type.includes('view')).sort())
        console.debug(types.filter(type => type === 'azure_sql_server'))
        console.debug(types.filter(type => type.includes('power')))
        console.debug(types.filter(type => type.includes('databricks')))
    })
    it('lineage', async () => {
        const targetViewName = 'vProductAndDescription'
        const r = await dataMap.assets({keywords: targetViewName});
        const vProductAndDescription = r.find(({qualifiedName}) => qualifiedName.endsWith(targetViewName))
        console.debug("vProductAndDescription", vProductAndDescription.id)

        await dataMap.lineageCreate({
            ...vProductAndDescription,
            upstreams: [
                '16f9dde3-e1a1-43a0-a9da-88f6f6f60000', // table name:Product
                'e8279254-5571-42bb-b6e3-5ff6f6f60000' // table name:ProductDescription
            ],
        })

    })
    it('asset list', async () => {
        const r = await dataMap.assets();
        assert.equal(r.length, 37)
        const allowedTypes = new Set(['Tables', 'Folders', undefined]);
        r.forEach(item => {
            assert(allowedTypes.has(item.objectType), `Unexpected value: ${item}`);
        });
        const tables = r.filter(({objectType}) => objectType === 'Tables')
        const Folders = r.filter(({objectType}) => objectType === 'Folders')
        const unknown = r.filter(({objectType}) => objectType === undefined)
        fs.writeFileSync('test/Tables.json', JSONReadable(tables))
        fs.writeFileSync('test/Folders.json', JSONReadable(Folders))
        fs.writeFileSync('test/undefined.json', JSONReadable(unknown))
        const process = r.find(({entityType}) => entityType === 'Process')
        console.debug(process)
    })
    it('asset search', async () => {
        const name = 'vProductAndDescription'
        const r = await dataMap.assets({keywords: name});
        console.debug(r)

    })
    it('entity list', async () => {
        // TODO empty result
        const r = await dataMap.entityList('azure_sql_server')
        console.debug(r)
    })
    it('entity get', async () => {
        const id = '3951385f-8495-4618-a913-a8f6f6f60000'
        const r = await dataMap.entityShow(id)
        console.debug(r.entity)
        console.info(r.entity.relationshipAttributes.sources)
    })

})