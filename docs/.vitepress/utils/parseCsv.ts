import fs from 'node:fs'
import { parse } from 'csv-parse/sync'

export interface CsvData {
  columns: string[]
  rows: Record<string, string>[]
}

export function parseCsvFile(filePath: string): CsvData {
  const content = fs.readFileSync(filePath, 'utf-8').replace(/^\uFEFF/, '')
  const rows = parse(content, {
    columns: true,
    skip_empty_lines: true,
    trim: true,
  }) as Record<string, string>[]

  return {
    columns: rows.length > 0 ? Object.keys(rows[0]) : [],
    rows,
  }
}