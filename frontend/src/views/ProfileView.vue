<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'

const router = useRouter()
const user = useUserStore()

const orders = ref([])
const favorites = ref([])
const loading = ref(true)
const name = ref('')
const phone = ref('')
const saved = ref(false)

function formatTicketType(type) {
    const map = {
        'dancefloor': 'Танцпол',
        'fan-zone': 'Фан-зона',
        'vip': 'VIP'
    }
    return map[type] || type
}

onMounted(async () => {
    if (!user.isLoggedIn) {
        router.push('/login')
        return
    }
    await user.loadProfile()
    name.value = user.profile?.name || ''
    phone.value = user.profile?.phone || ''

    try {
        const { data } = await api.getMyOrders()
        orders.value = data
    } catch (e) {
        console.error(e)
    }

    try {
        const { data: favData } = await api.getMyFavorites()
        favorites.value = favData
    } catch (e) {
        console.error(e)
    }

    loading.value = false
})

async function saveProfile() {
    await user.updateProfile({ name: name.value, phone: phone.value })
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
}

function logout() {
    user.logout()
    router.push('/')
}
</script>

<template>
    <div>
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Личный кабинет</h2>
                <button @click="logout" class="clear-search">Выйти</button>
            </div>

            <p>Email: <strong>{{ user.profile?.email }}</strong></p>

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
                        <strong>Заказ #{{ o.order_number }}</strong>
                        <p>{{ formatTicketType(o.ticket_type) }} — {{ o.quantity }} шт.</p>
                        <p>Сумма: {{ o.total_price }} ₽</p>
                        <p>Дата: {{ new Date(o.order_date).toLocaleString('ru') }}</p>
                    </div>
                </div>
            </div>

            <div class="orders-section">
                <h3>Избранные концерты</h3>
                <div v-if="!favorites.length" class="no-results">
                    <p>У вас пока нет избранных концертов</p>
                </div>
                <div v-else class="orders-list">
                    <div v-for="f in favorites" :key="f.id" class="order-item">
                        <strong>{{ f.artist.name }}</strong>
                        <p>{{ f.venue.city }}, {{ f.venue.name }}</p>
                        <p>{{ new Date(f.start_time).toLocaleString('ru') }}</p>
                        <p>Цена: от {{ f.min_price }} ₽</p>
                        <router-link :to="`/concert/${f.id}`" class="buy-button" style="margin-top: 10px; display: inline-block;">
                            Купить билет
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
    </div>
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