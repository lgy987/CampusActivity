<script setup lang="ts">
    import { AppButton, AppCard, AppPageContainer } from '@/components'
    import Topbar from '@/layouts/Topbar.vue'
    import router from '@/router'
</script>


<template>
<AppPageContainer>
  <Topbar />
  <router-link to="/Components/AppButtonDisplay"><AppButton>AppButton</AppButton></router-link>
  <router-link to="/Components/AppCardDisplay"><AppButton>AppCard</AppButton></router-link>
  <AppCard>
    <div>
      <router-view />
    </div>
  </AppCard>
</AppPageContainer>
</template>


