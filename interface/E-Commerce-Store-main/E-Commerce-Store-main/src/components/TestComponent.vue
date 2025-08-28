<template>
  <div style="position: fixed; top: 50px; left: 10px; background: green; color: white; padding: 10px; z-index: 10000;">
    Test Component Working - {{ message }}
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const message = ref('Hello World!')
</script>
