<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const props = defineProps({ concert: Object })
const router = useRouter()

const form = ref({
    name: '',
    email: '',
    phone: '',
    ticket_type: '',
    ticket_id: '',
    quantity: 1,
})
const error = ref('')
const loading = ref(false)

async function submit() {
    error.value = ''
    loading.value = true
    try {
        const { data } = await api.buyTicket(props.concert.id, form.value)
        router.push({ name: 'order-success', params: { id: data.id } })
    } catch (e) {
        error.value = e.response?.data?.error || 'Ошибка при оформлении заказа'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="ticket-form">
        <form @submit.prevent="submit">
            <input
                v-model="form.name"
                type="text"
                placeholder="Имя"
                required
                class="form-input"
            >
            <input
                v-model="form.email"
                type="email"
                placeholder="Email"
                required
                class="form-input"
            >
            <input
                v-model="form.phone"
                type="tel"
                placeholder="Телефон"
                required
                class="form-input"
            >

            <select v-model="form.ticket_type" class="form-input" required>
                <option value="">Выберите тип билета</option>
                <option value="dancefloor">Танцпол</option>
                <option value="fan-zone">Фан-зона</option>
                <option value="vip">VIP</option>
            </select>

            <select v-model="form.ticket_id" class="form-input" required>
                <option value="">Выберите категорию билета</option>
                <option
                    v-for="t in concert.tickets"
                    :key="t.id"
                    :value="t.id"
                >
                    {{ t.category.name }} - {{ t.price }} ₽
                    (доступно: {{ t.quantity }})
                </option>
            </select>

            <select v-model.number="form.quantity" class="form-input" required>
                <option value="1">1 билет</option>
                <option value="2">2 билета</option>
                <option value="3">3 билета</option>
                <option value="4">4 билета</option>
                <option value="5">5 билетов</option>
            </select>

            <button
                type="submit"
                class="submit-btn"
                :disabled="loading"
            >
                {{ loading ? 'Отправка...' : 'Забронировать билеты' }}
            </button>

            <p v-if="error" style="color: red; margin-top: 10px;">
                {{ error }}
            </p>
        </form>
    </div>
</template>