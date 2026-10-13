<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selected = ref('')

function goTo(value) {
    if (!value) return
    router.push({ path: '/', hash: `#${value}` })
    selected.value = ''
}
</script>

<template>
    <header class="header">
        <router-link to="/" class="logo">SOUNDSTAGE</router-link>

        <nav class="nav">
            <router-link to="/">Главная</router-link>
            <router-link to="/tickets">Билеты</router-link>
        </nav>

        <div class="header-actions">
            <select class="city-select" v-model="selected" @change="goTo(selected)">
                <option value="">Выберите что нужно</option>
                <option value="concerts">Концерты</option>
                <option value="artists">Артисты</option>
                <option value="cities">Площадки</option>
            </select>
        </div>
    </header>
</template>