import {DataMap} from "../data-map.js";
import {typeName} from "../format/const.js"

const {mssql: {table, view}} = typeName
const targetViewName = 'mssql://always-free.database.windows.net/app-kyndryl-hk/SalesLT/vProductAndDescription'
const sourceTable1 = 'mssql://always-free.database.windows.net/app-kyndryl-hk/SalesLT/Product'
const sourceTable2 = 'mssql://always-free.database.windows.net/app-kyndryl-hk/SalesLT/ProductDescription'
const sourceTableType = table
const targetViewType = view
describe('', function () {
    this.timeout(0)
    const dataMap = new DataMap()
    it('table2view lineage', async () => {

        const t1 = await dataMap.entityGet(sourceTableType, sourceTable1)
        const t2 = await dataMap.entityGet(sourceTableType, sourceTable2)
        const vProductAndDescription = await dataMap.entityGet(targetViewType, targetViewName)


        const {guid, name, qualifiedName, entityType} = vProductAndDescription
        const r = await dataMap.lineageCreate({
            guid, name, qualifiedName, entityType,
            upstreams: [
                {
                    guid: t1.guid,
                }, // table name:Product
                {
                    guid: t2.guid
                } // table name:ProductDescription
            ],
        })
        console.debug(r)
    })
})