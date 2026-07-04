import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { scanResultTree } from '../.vitepress/utils/scanResult'

const resultRoot = path.dirname(fileURLToPath(import.meta.url))

export default {
  watch: ['./*/'],
  load() {
    return { versions: scanResultTree(resultRoot) }
  },
}