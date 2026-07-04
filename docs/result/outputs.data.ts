import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { benchOutputKey, scanResultTree } from '../.vitepress/utils/scanResult'
import { parseCsvFile } from '../.vitepress/utils/parseCsv'
import type { CsvData } from '../.vitepress/utils/parseCsv'

const resultRoot = path.dirname(fileURLToPath(import.meta.url))

export default {
  watch: ['./*/*/result_combine.csv'],
  load(files: string[]) {
    const outputs: Record<string, CsvData> = {}

    for (const file of files) {
      const relativeDir = path.relative(resultRoot, path.dirname(file))
      outputs[relativeDir] = parseCsvFile(file)
    }

    for (const version of scanResultTree(resultRoot)) {
      for (const model of version.models) {
        if (!model.hasOutput) continue
        const key = benchOutputKey(version.version, model.name)
        outputs[key] ??= { columns: [], rows: [] }
      }
    }

    return outputs
  },
}