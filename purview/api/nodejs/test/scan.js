import Scan from '../scan.js'
describe('scan', function () {
    this.timeout(0)
    it('sources', async () => {
        const scan = new Scan()
        const sources = await scan.sources()
        console.debug(sources)
    })
})