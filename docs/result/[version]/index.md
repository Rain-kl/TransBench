---
title: 版本概览
---

<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'
import { data } from '../index.data'

const { params } = useData()

const version = computed(() =>
  data.versions.find((item) => item.version === params.value.version),
)

const versionName = computed(() => params.value.version)
</script>

# {{ versionName }}

<VersionIndex v-if="version" :version="version" />