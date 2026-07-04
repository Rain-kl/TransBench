<script setup lang="ts">
import type { ExamVersion } from '../../utils/scanResult'

defineProps<{
  versions: ExamVersion[]
}>()
</script>

<template>
  <p>
    各基准模型的评测结果按 <strong>试题版本 → 基准模型</strong> 归档。不同版本使用不同试题集与裁判模型，
    <strong>结果仅供查阅，不作横向排名</strong>。
  </p>

  <h2>试题版本</h2>
  <table>
    <thead>
      <tr>
        <th>版本</th>
        <th>基准模型数</th>
        <th>exam.md</th>
        <th>prompt.md</th>
        <th>入口</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="version in versions" :key="version.version">
        <td>
          <a :href="`/result/${version.version}/`">{{ version.version }}</a>
        </td>
        <td>{{ version.models.length }}</td>
        <td>
          <a v-if="version.hasExam" :href="`/result/${version.version}/exam`">exam.md</a>
          <span v-else>—</span>
        </td>
        <td>
          <a v-if="version.hasPrompt" :href="`/result/${version.version}/prompt`">prompt.md</a>
          <span v-else>—</span>
        </td>
        <td>
          <a :href="`/result/${version.version}/`">查看</a>
        </td>
      </tr>
    </tbody>
  </table>

  <section v-for="version in versions" :key="version.version">
    <h2>{{ version.version }}</h2>
    <p v-if="version.hasExam || version.hasPrompt">
      <template v-if="version.hasExam">
        <a :href="`/result/${version.version}/exam`">exam.md</a>
      </template>
      <template v-if="version.hasExam && version.hasPrompt"> · </template>
      <template v-if="version.hasPrompt">
        <a :href="`/result/${version.version}/prompt`">prompt.md</a>
      </template>
    </p>
    <table>
      <thead>
        <tr>
          <th>基准模型</th>
          <th>裁判模型</th>
          <th>输出结果</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="model in version.models" :key="model.name">
          <td>{{ model.name }}</td>
          <td>
            <span v-for="(judge, index) in model.judges" :key="judge">
              <a :href="`/result/${version.version}/${model.name}/${judge}`">{{ judge }}</a>
              <span v-if="index < model.judges.length - 1"> · </span>
            </span>
          </td>
          <td>
            <a
              v-if="model.hasOutput"
              :href="`/result/${version.version}/${model.name}/output`"
            >输出结果</a>
            <span v-else>—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>