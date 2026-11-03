<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const user = useUserStore()
const email = ref('')
const password = ref('')
const name = ref('')
const phone = ref('')
const error = ref('')

async function submit() {
    error.value = ''
    try {
        await user.register({
            email: email.value,
            password: password.value,
            name: name.value,
            phone: phone.value,
        })
        router.push('/login')
    } catch (e) {
        error.value = e.response?.data?.error || 'Ошибка регистрации'
    }
}
</script>

<template>
    <section class="section" style="max-width: 500px; margin: 100px auto;">
        <h1 class="section-title">Регистрация</h1>
        <form @submit.prevent="submit">
            <input v-model="email" type="email" placeholder="Email" required class="form-input" style="margin-top: 20px;">
            <input v-model="password" type="password" placeholder="Пароль" required class="form-input" style="margin-top: 10px;">
            <input v-model="name" placeholder="Имя" class="form-input" style="margin-top: 10px;">
            <input v-model="phone" placeholder="Телефон" class="form-input" style="margin-top: 10px;">
            <button type="submit" class="submit-btn" style="margin-top: 15px;">Зарегистрироваться</button>
            <p v-if="error" style="color: red; margin-top: 10px;">{{ error }}</p>
            <p style="margin-top: 15px; text-align: center;">
                Уже есть аккаунт? <router-link to="/login">Войти</router-link>
            </p>
        </form>
    </section>
</template>