<script setup lang="ts">
    import { AppButton, AppCard, AppPageContainer } from '@/components'
    import Topbar from '@/layouts/Topbar.vue'
    import router from '@/router'
</script>


<template>
<AppPageContainer variant="light">
  <Topbar />
  <div>
    <router-link to="/Components/AppButtonDisplay"><AppButton>AppButton</AppButton></router-link>
    <router-link to="/Components/AppCardDisplay"><AppButton>AppCard</AppButton></router-link>
    <router-link to="/Components/AppPageContainerDisplay"><AppButton>AppPageContainer</AppButton></router-link>
    <router-link to="/Components/AppDialogDisplay"><AppButton>AppDialog</AppButton></router-link>
    <router-link to="/Components/AppInputDisplay"><AppButton>AppInput</AppButton></router-link>
    <router-link to="/Components/AppFormDisplay"><AppButton>AppForm</AppButton></router-link>
  </div>
  <AppCard variant="color-bg" color="rgb(250,250,250)">
    <div style="min-width: 1000px; width: 100%;">
      <router-view />
    </div>
  </AppCard>
</AppPageContainer>
</template>


