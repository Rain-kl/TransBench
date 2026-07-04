<script setup lang="ts">
import { computed, ref } from 'vue'

const props = defineProps<{
  rows: Record<string, string>[]
  columns?: string[]
}>()

const query = ref('')

const columns = computed(() => {
  if (props.columns?.length) return props.columns
  return props.rows.length > 0 ? Object.keys(props.rows[0]) : []
})

const filteredRows = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return props.rows
  return props.rows.filter((row) =>
    columns.value.some((col) => row[col]?.toLowerCase().includes(q)),
  )
})
</script>

<template>
  <div class="csv-table">
    <div class="csv-table__toolbar">
      <input
        v-model="query"
        class="csv-table__search"
        type="search"
        placeholder="搜索原文或译文…"
      />
      <span class="csv-table__count">
        {{ filteredRows.length }} / {{ rows.length }} 条
      </span>
    </div>
    <div class="csv-table__wrapper">
      <table>
        <thead>
          <tr>
            <th class="csv-table__index">#</th>
            <th v-for="col in columns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in filteredRows" :key="index">
            <td class="csv-table__index">{{ index + 1 }}</td>
            <td v-for="col in columns" :key="col">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.csv-table {
  margin: 1rem 0 2rem;
}

.csv-table__toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.csv-table__search {
  flex: 1;
  max-width: 320px;
  padding: 0.45rem 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  font-size: 0.9rem;
}

.csv-table__search:focus {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 1px;
}

.csv-table__count {
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
  white-space: nowrap;
}

.csv-table__wrapper {
  overflow: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.88rem;
}

th,
td {
  padding: 0.65rem 0.85rem;
  border-bottom: 1px solid var(--vp-c-divider);
  text-align: left;
  vertical-align: top;
}

th {
  position: sticky;
  top: 0;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-weight: 600;
  white-space: nowrap;
}

tbody tr:hover {
  background: var(--vp-c-bg-soft);
}

.csv-table__index {
  width: 3rem;
  color: var(--vp-c-text-3);
  text-align: center;
  white-space: nowrap;
}
</style>