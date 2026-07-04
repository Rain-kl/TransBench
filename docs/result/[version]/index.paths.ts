import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { scanResultTree } from '../../.vitepress/utils/scanResult'

const resultRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

export default {
  paths() {
    return scanResultTree(resultRoot).map((version) => ({
      params: { version: version.version },
    }))
  },
}