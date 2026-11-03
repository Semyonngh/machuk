<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const user = useUserStore()
const email = ref('')
const password = ref('')
const error = ref('')

async function submit() {
    error.value = ''
    try {
        await user.login(email.value, password.value)
        router.push('/profile')
    } catch (e) {
        error.value = 'Неверный email или пароль'
    }
}
</script>

<template>
    <section class="section" style="max-width: 500px; margin: 100px auto;">
        <h1 class="section-title">Вход</h1>
        <form @submit.prevent="submit">
            <input v-model="email" type="email" placeholder="Email" required class="form-input" style="margin-top: 20px;">
            <input v-model="password" type="password" placeholder="Пароль" required class="form-input" style="margin-top: 10px;">
            <button type="submit" class="submit-btn" style="margin-top: 15px;">Войти</button>
            <p v-if="error" style="color: red; margin-top: 10px;">{{ error }}</p>
            <p style="margin-top: 15px; text-align: center;">
                Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
            </p>
        </form>
    </section>
</template>