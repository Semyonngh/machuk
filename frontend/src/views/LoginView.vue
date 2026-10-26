<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const user = useUserStore()
const email = ref('')

function submit() {
    if (!email.value) return
    user.login(email.value)
    router.push('/profile')
}
</script>

<template>
    <section class="section" style="max-width: 500px; margin: 100px auto;">
        <h1 class="section-title">Вход в личный кабинет</h1>
        <p>Введите email, который использовали при покупке билетов</p>
        <form @submit.prevent="submit">
            <input
                v-model="email"
                type="email"
                placeholder="Ваш email"
                required
                class="form-input"
                style="margin-top: 20px;"
            >
            <button type="submit" class="submit-btn" style="margin-top: 15px;">
                Войти
            </button>
        </form>
    </section>
</template>