import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import CsvTable from './components/CsvTable.vue'
import ResultIndex from './components/ResultIndex.vue'
import VersionIndex from './components/VersionIndex.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('CsvTable', CsvTable)
    app.component('ResultIndex', ResultIndex)
    app.component('VersionIndex', VersionIndex)
  },
} satisfies Theme