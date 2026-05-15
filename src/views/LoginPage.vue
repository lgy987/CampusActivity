<script setup lang="ts">
    import { AppButton, AppCard, AppPageContainer } from '@/components'
    import Topbar from '@/layouts/Topbar.vue'
    import router from '@/router'

    function goToComponentsDisplay() {
      router.push('Components')
    }
</script>


<template>
<AppPageContainer>
  <Topbar />
  <AppCard>
    <div>
      <p>欢迎来到CampusActivity</p>
    </div>
    <AppButton @click="goToComponentsDisplay">组件展示页</AppButton>
  </AppCard>
</AppPageContainer>
</template>


