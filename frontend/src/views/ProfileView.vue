<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'

const router = useRouter()
const user = useUserStore()

const orders = ref([])
const loading = ref(true)
const name = ref(user.name)
const phone = ref(user.phone)
const saved = ref(false)

onMounted(async () => {
    if (!user.isLoggedIn) {
        router.push('/login')
        return
    }
    await user.loadProfile()
    name.value = user.name
    phone.value = user.phone

    try {
        const { data } = await api.getOrdersByEmail(user.email)
        orders.value = data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
})

async function saveProfile() {
    await user.updateProfile(name.value, phone.value)
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
}

function logout() {
    user.logout()
    router.push('/')
}
</script>

<template>
    <section class="section">
        <div class="section-header">
            <h2 class="section-title">Личный кабинет</h2>
            <button @click="logout" class="clear-search">Выйти</button>
        </div>

        <p>Email: <strong>{{ user.email }}</strong></p>

        <div class="profile-form">
            <h3>Редактировать профиль</h3>
            <input v-model="name" placeholder="Имя" class="form-input">
            <input v-model="phone" placeholder="Телефон" class="form-input">
            <button @click="saveProfile" class="submit-btn">
                {{ saved ? 'Сохранено!' : 'Сохранить' }}
            </button>
        </div>

        <div class="orders-section">
            <h3>История заказов</h3>
            <div v-if="loading">Загрузка...</div>
            <div v-else-if="!orders.length" class="no-results">
                <p>У вас пока нет заказов</p>
            </div>
            <div v-else class="orders-list">
                <div v-for="o in orders" :key="o.id" class="order-item">
                    <div>
                        <strong>Заказ #{{ o.order_number }}</strong>
                        <p>{{ o.ticket_type }} — {{ o.quantity }} шт.</p>
                        <p>Сумма: {{ o.total_price }} ₽</p>
                        <p>Дата: {{ new Date(o.order_date).toLocaleString('ru') }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="orders-section">
            <h3>Избранные концерты</h3>
            <p v-if="!user.favorites.length">Пока пусто</p>
            <p v-else>У вас {{ user.favorites.length }} избранных концертов</p>
        </div>
    </section>
</template>

<style scoped>
.profile-form {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin: 30px 0;
    max-width: 500px;
}
.orders-section {
    margin-top: 30px;
}
.order-item {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>