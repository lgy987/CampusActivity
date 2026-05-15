<script setup lang="ts">
    import { AppNavbar } from '@/components'
</script>

<template>
    <AppNavbar brand-name="CampusActivity"
                   :nav-items="[
      { label: '首页', href: '/' },
      { label: '关于', href: '/about' },
      { label: '联系', href: '/contact' }
    ]" />
</template>