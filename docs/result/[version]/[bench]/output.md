---
title: 输出结果
---

<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'
import { data as outputs } from '../../outputs.data'

const { params } = useData()

const key = computed(() => {
  const { version, bench } = params.value
  return `${version}/${bench}`
})

const data = computed(() => outputs[key.value] ?? { columns: [], rows: [] })
const bench = computed(() => params.value.bench)
</script>

# {{ bench }} · 输出结果

翻译输出来源：`result_combine.csv`（构建时加载，共 {{ data.rows.length }} 条）

<CsvTable :rows="data.rows" :columns="data.columns" />