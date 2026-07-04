import fs from 'node:fs'
import path from 'node:path'

export interface BenchModel {
  name: string
  judges: string[]
  hasOutput: boolean
}

export interface ExamVersion {
  version: string
  hasExam: boolean
  hasPrompt: boolean
  models: BenchModel[]
}

const VERSION_RE = /^v\d+\.\d+\.\d+$/
const VERSION_FILES = {
  exam: 'exam.md',
  prompt: 'prompt.md',
} as const

export function scanResultTree(resultRoot: string): ExamVersion[] {
  if (!fs.existsSync(resultRoot)) return []

  return fs
    .readdirSync(resultRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && VERSION_RE.test(entry.name))
    .map((entry) => entry.name)
    .sort((a, b) => b.localeCompare(a, undefined, { numeric: true }))
    .map((version) => {
      const versionDir = path.join(resultRoot, version)
      return {
        version,
        hasExam: fs.existsSync(path.join(versionDir, VERSION_FILES.exam)),
        hasPrompt: fs.existsSync(path.join(versionDir, VERSION_FILES.prompt)),
        models: scanBenchModels(versionDir),
      }
    })
}

function scanBenchModels(versionDir: string): BenchModel[] {
  return fs
    .readdirSync(versionDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => {
      const benchDir = path.join(versionDir, entry.name)
      const judges = fs
        .readdirSync(benchDir)
        .filter((file) => file.endsWith('.md'))
        .map((file) => file.replace(/\.md$/, ''))
        .sort()

      return {
        name: entry.name,
        judges,
        hasOutput: fs.existsSync(path.join(benchDir, 'result_combine.csv')),
      }
    })
    .sort((a, b) => a.name.localeCompare(b.name))
}

export function benchOutputKey(version: string, bench: string): string {
  return `${version}/${bench}`
}