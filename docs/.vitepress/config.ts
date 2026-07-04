import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { defineConfig } from 'vitepress'
import { buildResultNavItems, buildResultSidebars } from './utils/buildResultNav'
import { scanResultTree } from './utils/scanResult'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const resultRoot = path.resolve(__dirname, '../result')
const resultVersions = scanResultTree(resultRoot)

export default defineConfig({
  title: 'TransBench',
  description: '大模型中英翻译能力基准测试与评测结果',
  lang: 'zh-CN',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide/' },
      {
        text: '评测结果',
        items: buildResultNavItems(resultVersions),
      },
      {
        text: 'GitHub',
        link: 'https://github.com/Rain-kl/TransBench',
      },
    ],
    sidebar: {
      '/guide/': [
        {
          text: '指南',
          items: [
            { text: '概览', link: '/guide/' },
            { text: '快速入门', link: '/guide/getting-started' },
            { text: '评分标准', link: '/guide/scoring' },
            { text: '需求文档', link: '/guide/requirements' },
          ],
        },
      ],
      ...buildResultSidebars(resultVersions),
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Rain-kl/TransBench' },
    ],
    footer: {
      message: 'MIT Licensed',
      copyright: 'Copyright © TransBench Contributors',
    },
    search: {
      provider: 'local',
    },
  },
})