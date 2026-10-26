<script setup>
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'

const user = useUserStore()
const router = useRouter()
</script>

<template>
    <header class="header">
        <router-link to="/" class="logo">SOUNDSTAGE</router-link>

        <nav class="nav">
            <router-link to="/">Главная</router-link>
            <router-link to="/tickets">Билеты</router-link>
        </nav>

        <div class="header-actions">
            <button v-if="!user.isLoggedIn" @click="router.push('/login')" class="login-button">
                Войти
            </button>
            <button v-else @click="router.push('/profile')" class="login-button">
                Кабинет
            </button>
        </div>
    </header>
</template>