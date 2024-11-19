import {DataMap} from "../data-map.js";
import {typeName} from "../format/const.js"

const {mssql: {table, view}} = typeName
const db_endpoint = 'mssql://always-free.database.windows.net/app-kyndryl-hk'
const targetViewName = db_endpoint + '/SalesLT/vProductAndDescription'
const sourceTable_Product = db_endpoint + '/SalesLT/Product'
const sourceTable_ProductModel = db_endpoint + '/SalesLT/ProductModel'
const sourceTable_ProductDescription = db_endpoint + '/SalesLT/ProductDescription'
const sourceTable_ProductModelProductDescription = db_endpoint + '/SalesLT/ProductModelProductDescription'
const sourceTableType = table
const targetViewType = view
describe('', function () {
    this.timeout(0)
    const dataMap = new DataMap()
    let Product, ProductDescription, ProductModel, ProductModelProductDescription
    let vProductAndDescription
    before(async () => {
        vProductAndDescription = await dataMap.entityGet(targetViewType, targetViewName)
        // sources
        Product = await dataMap.entityGet(sourceTableType, sourceTable_Product)
        ProductModel = await dataMap.entityGet(sourceTableType, sourceTable_ProductModel)
        ProductDescription = await dataMap.entityGet(sourceTableType, sourceTable_ProductDescription)
        ProductModelProductDescription = await dataMap.entityGet(sourceTableType, sourceTable_ProductModelProductDescription)
    })
    it('table2view lineage', async () => {

        const {guid, name, qualifiedName, entityType} = vProductAndDescription
        const r = await dataMap.lineageCreate({
            guid, name, qualifiedName, entityType,
            upstreams: [
                Product.guid,
                ProductDescription.guid,
                ProductModel.guid,
                ProductModelProductDescription.guid,
            ],
        })
        console.debug(r)
    })
    it('column2view lineage', async () => {

        const r_Product = vProductAndDescription.relationBySourceId(Product.guid)
        const r_ProductModel = vProductAndDescription.relationBySourceId(ProductModel.guid)
        const r_ProductDescription = vProductAndDescription.relationBySourceId(ProductDescription.guid)
        const r_ProductModelProductDescription = vProductAndDescription.relationBySourceId(ProductModelProductDescription.guid)

        await dataMap.columnLineage(r_Product, {
            ProductID: '',
            Name: '',
        })
        await dataMap.columnLineage(r_ProductModel, {
            Name: 'ProductModel',
        })
        await dataMap.columnLineage(r_ProductModelProductDescription, {
            Culture: ''
        })
        await dataMap.columnLineage(r_ProductDescription, {
            Description: ''
        })


    })
})