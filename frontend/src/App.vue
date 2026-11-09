<script setup>
import { onMounted, ref, provide } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import Toast from './components/Toast.vue'
import { useUserStore } from './stores/user'

const toast = ref(null)
provide('toast', toast)

const user = useUserStore()

onMounted(() => {
    if (user.isLoggedIn && !user.profile) {
        user.loadProfile()
    }
})
</script>

<template>
    <AppHeader />
    <main class="main-content">
        <router-view v-slot="{ Component }">
            <transition name="page" mode="out-in">
                <component :is="Component" />
            </transition>
        </router-view>
    </main>
    <AppFooter />
    <Toast ref="toast" />
</template>