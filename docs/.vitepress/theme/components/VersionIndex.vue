<script setup lang="ts">
import type { ExamVersion } from '../../utils/scanResult'

defineProps<{
  version: ExamVersion
}>()
</script>

<template>
  <h2>版本文件</h2>
  <table>
    <thead>
      <tr>
        <th>文件</th>
        <th>说明</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="version.hasExam">
        <td><a :href="`/result/${version.version}/exam`">exam.md</a></td>
        <td>试题集</td>
      </tr>
      <tr v-if="version.hasPrompt">
        <td><a :href="`/result/${version.version}/prompt`">prompt.md</a></td>
        <td>评分提示词</td>
      </tr>
    </tbody>
  </table>

  <h2>基准模型</h2>
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
</template>