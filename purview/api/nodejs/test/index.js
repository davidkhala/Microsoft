import assert from 'assert'
import {Account} from '../account.js'
import {DataMap} from "../data-map.js";
import {entityType} from '../format/const.js'
import {JSONReadable} from '@davidkhala/light/format.js'
import fs from 'fs'

const {mssql: {view}} = entityType
const tenantID = "c2a38aca-e9c7-4647-8dcd-9185476159ae"
const subscription = "d02180af-0630-4747-ab1b-0d3b3c12dafb"
const defaultAccountName = "admin-david"
describe('account', function () {
    this.timeout(0)
    const account = new Account()
    it('default account', async () => {
        const {accountName} = await account.defaultAccount(tenantID, subscription)
        assert.equal(accountName, defaultAccountName)
    })
    it('collections', async () => {
        const r = await account.collections()
        console.debug(r)
    })
})
describe('data map', function () {
    this.timeout(0)
    const dataMap = new DataMap()
    it('types', async () => {
        const result = await dataMap.types()
        console.debug(result)
    })
    it('entityTypes', async () => {
        const types = await dataMap.entityTypes()
        console.debug(types.filter(type => type.includes('view')).sort())
        console.debug(types.filter(type => type === 'azure_sql_server'))
        console.debug(types.filter(type => type.includes('power')))
        console.debug(types.filter(type => type.includes('databricks')))
    })
    it('asset search', async () => {

        console.debug(await dataMap.assets({keywords: 'vProductAndDescription'}));
        console.debug(await dataMap.assets({keywords: '*'}))

    })

    it('asset list', async () => {
        const r = await dataMap.assets();
        const allowedTypes = new Set(['Tables', 'Folders', 'Reports', 'Stored procedures', undefined]);
        r.forEach(item => {
            assert(allowedTypes.has(item.objectType), `Unexpected value: ${item.objectType}`);
            const segment = r.filter(({objectType}) => objectType === item.objectType);
            fs.writeFileSync(`test/artifacts/${item.objectType}.json`, JSONReadable(segment))
        });

    })

    it('relation set', async () => {
        const id = 'e2323179-19d1-475a-aeb3-8244507161cb'
        const columns = {
            Name: '', ProductID: ''
        }

        await dataMap.columnLineage(id, columns)
    })
    it('entity get', async () => {
        const id = 'fc01fdae-c360-4c23-910a-39f6f6f60000'
        const r = await dataMap.entityShow(id)
        const {sources, sinks} = r.relationship

        console.debug(sources)
        const relation_id = sources[0].relationshipGuid
        const relation = await dataMap.relationShow(relation_id)
        console.debug("------source[0]")
        console.info(relation)

    })

    it('entity delete', async () => {
        const id = '3fc7b4b0-def4-470c-a27a-8cddb4e0639f'
        const r = await dataMap.entityDelete(id)
        console.debug(r)
    })
    it('entity get by attrs', async () => {
        const fullName = 'mssql://always-free.database.windows.net/app-kyndryl-hk/SalesLT/vProductAndDescription'
        const entity = await dataMap.entityGet(view, fullName)

        const sources = entity.upstream_relations

        const r = await dataMap.relationShow(sources[0])
        console.debug(r)
        const l = await dataMap.lineageGet(entity.guid)
        console.debug(l)  // Don't have too much info
    })

})