<script setup>
import { ref, provide } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import Toast from './components/Toast.vue'

const toast = ref(null)
provide('toast', toast)
</script>

<template>
    <AppHeader />
    <main class="main-content">
        <router-view />
    </main>
    <AppFooter />
    <Toast ref="toast" />
</template>