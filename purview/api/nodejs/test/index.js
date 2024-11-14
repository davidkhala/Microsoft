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
                {
                    guid: '16f9dde3-e1a1-43a0-a9da-88f6f6f60000',
                    columns: {
                        Name: 'Name'
                    }
                }, // table name:Product
                {
                    guid: 'e8279254-5571-42bb-b6e3-5ff6f6f60000'
                } // table name:ProductDescription
            ],
        })

    })
    it('asset list', async () => {
        const r = await dataMap.assets();
        assert.equal(r.length, 36)
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

        console.debug(await dataMap.assets({keywords: 'vProductAndDescription'}));
        console.debug(await dataMap.assets({keywords: '*'}))

    })
    it('relation get', async () => {
        const id = '252b29a4-90c6-47b4-b169-6c55ef984f68'
        const r = await dataMap.relationShow(id)
        console.debug(r)
    })
    it('relation set', async () => {
        const id = '252b29a4-90c6-47b4-b169-6c55ef984f68'
        const columns = {
            Name: 'Name'
        }
        await dataMap.columnLineage(id, columns)
    })
    it('entity get', async () => {
        const id = '1a8fdc43-73c9-4abe-83ea-40f6f6f60000'
        const r = await dataMap.entityShow(id)
        // console.debug(r.entity)
        const {sources, sinks} = r.entity.relationshipAttributes
        const s1 = sources.find(({displayText}) => displayText === 'Product')
        console.debug(s1)
        const s2 = sources.find(({displayText}) => displayText === 'ProductDescription')
        console.debug(s2)

        const k1 = sinks.find(({displayText}) => displayText === 'Product')
        console.debug(k1)

    })

})