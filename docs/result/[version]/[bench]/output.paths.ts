import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { scanResultTree } from '../../../.vitepress/utils/scanResult'

const resultRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')

export default {
  paths() {
    return scanResultTree(resultRoot).flatMap((version) =>
      version.models
        .filter((model) => model.hasOutput)
        .map((model) => ({
          params: {
            version: version.version,
            bench: model.name,
          },
        })),
    )
  },
}