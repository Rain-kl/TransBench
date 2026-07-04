import type { DefaultTheme } from 'vitepress'
import type { ExamVersion } from './scanResult'

type SidebarItem = DefaultTheme.SidebarItem

export function buildResultNavItems(versions: ExamVersion[]) {
  return [
    { text: '模型索引', link: '/result/' },
    ...versions.map((v) => ({
      text: v.version,
      link: `/result/${v.version}/`,
    })),
  ]
}

export function buildResultSidebars(versions: ExamVersion[]): Record<string, SidebarItem[]> {
  const sidebars: Record<string, SidebarItem[]> = {
    '/result/': [{ text: '模型索引', link: '/result/' }],
  }

  for (const version of versions) {
    const versionItems: SidebarItem[] = [
      { text: '模型索引', link: '/result/' },
      { text: '版本概览', link: `/result/${version.version}/` },
    ]

    if (version.hasExam) {
      versionItems.push({
        text: 'exam.md',
        link: `/result/${version.version}/exam`,
      })
    }

    if (version.hasPrompt) {
      versionItems.push({
        text: 'prompt.md',
        link: `/result/${version.version}/prompt`,
      })
    }

    sidebars[`/result/${version.version}/`] = [
      ...versionItems,
      ...version.models.map((model) => ({
        text: model.name,
        collapsed: false,
        items: [
          ...model.judges.map((judge) => ({
            text: judge,
            link: `/result/${version.version}/${model.name}/${judge}`,
          })),
          ...(model.hasOutput
            ? [{ text: '输出结果', link: `/result/${version.version}/${model.name}/output` }]
            : []),
        ],
      })),
    ]
  }

  return sidebars
}