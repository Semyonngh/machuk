<script setup>
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
</script>

<template>
    <AppHeader />
    <main class="main-content">
        <router-view />
    </main>
    <AppFooter />
</template>