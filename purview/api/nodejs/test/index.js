import {Types} from '../types.js'
import {API} from '../index.js'

describe('', function () {
    this.timeout(0)
    it('context', async () => {
        const tenantID = "c2a38aca-e9c7-4647-8dcd-9185476159ae"
        const api = new API()
        await api.defaultAccount(tenantID)
    })
    it('types', async () => {
        const t = new Types()
        await t.list()
    })
})