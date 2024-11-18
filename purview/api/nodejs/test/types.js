import {DataMap} from "../data-map.js";
import assert from "assert";
import fs from "fs";
import {JSONReadable} from '@davidkhala/light/format.js'

describe('analysis prebuilt types', function () {
    this.timeout(0)
    const dataMap = new DataMap()
    let types
    before(async () => {
        types = await dataMap.types()
    })
    it('enumDefs are const for Purview internal usage only', async () => {
        const {enumDefs} = types
        fs.writeFileSync('test/artifacts/enumDefs.json', JSONReadable(enumDefs))
    })
    it('structDefs', async () => {
        const {structDefs} = types
        for (const structDef of structDefs) {
            assert.deepStrictEqual(structDef.category, 'STRUCT')
        }
        fs.writeFileSync('test/artifacts/structDefs.json', JSONReadable(structDefs))
    })
    it('classificationDefs', async () => {
        const {classificationDefs} = types
        const names = []

        for (const classificationDef of classificationDefs) {
            assert.deepStrictEqual(classificationDef.category, 'CLASSIFICATION')
            names.push(classificationDef.description)
        }
        fs.writeFileSync('test/artifacts/classificationDefs.json', JSONReadable(names))
    })
    it('entityDefs', async () => {
        const {entityDefs} = types
        fs.writeFileSync('test/artifacts/entityDefs.json', JSONReadable(entityDefs.map(({name}) => name)))
    })
    it('relationshipDefs', async () => {
        const {relationshipDefs} = types
        fs.writeFileSync('test/artifacts/relationshipDefs.json', JSONReadable(relationshipDefs.map(({name}) => name)))

    })
    it("termTemplateDefs", async () => {
        const {termTemplateDefs} = types
        assert.equal(termTemplateDefs.length, 0, 'found termTemplateDefs')
    })
    it('businessMetadataDefs', async () => {
        const {businessMetadataDefs} = types
        const PurviewDataQuality = businessMetadataDefs[0]
        console.debug(PurviewDataQuality)
        assert.equal(PurviewDataQuality.name, 'PurviewDataQuality')
        assert.equal(businessMetadataDefs.length, 1, 'found businessMetadataDefs')
    })

})