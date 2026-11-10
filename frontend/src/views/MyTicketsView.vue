<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'
import QRCode from 'qrcode'

const router = useRouter()
const user = useUserStore()
const toast = inject('toast')
const tickets = ref([])
const loading = ref(true)

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

    try {
        const { data } = await api.getMyTickets()
        const withQr = await Promise.all(data.map(async (t) => {
            const qrText = `Заказ: ${t.order_number}\nБилет: ${formatTicketType(t.ticket_type)}\nКол-во: ${t.quantity}`
            const qr = await QRCode.toDataURL(qrText)
            return { ...t, qr }
        }))
        tickets.value = withQr
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div>
        <section class="section">
            <div class="section-header">
                <h2 class="section-title">Мои билеты</h2>
            </div>

            <div v-if="loading" class="no-results"><p>Загрузка...</p></div>

            <div v-else-if="!tickets.length" class="no-results">
                <h3>У вас пока нет купленных билетов</h3>
                <router-link 
                    :to="user.isLoggedIn ? '/tickets' : '/login'" 
                    class="cta-button"
                >
                    Купить билеты
                </router-link>
            </div>

            <div v-else class="tickets-grid">
                <div v-for="t in tickets" :key="t.id" class="ticket-card">
                    <div class="ticket-header">
                        <span class="ticket-number">#{{ t.order_number }}</span>
                        <span class="ticket-type">{{ formatTicketType(t.ticket_type) }}</span>
                    </div>

                    <div class="ticket-body">
                        <div class="ticket-qr">
                            <img :src="t.qr" alt="QR-код билета">
                        </div>
                        <div class="ticket-info">
                            <p><strong>Количество:</strong> {{ t.quantity }} шт.</p>
                            <p><strong>Сумма:</strong> {{ t.total_price }} ₽</p>
                            <p><strong>Дата:</strong> {{ new Date(t.order_date).toLocaleString('ru') }}</p>
                            <p><strong>Email:</strong> {{ t.email }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.tickets-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
}

.ticket-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.ticket-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.ticket-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #eee;
}

.ticket-number {
    font-weight: bold;
    font-size: 1.1rem;
}

.ticket-type {
    background: #000;
    color: #fff;
    padding: 0.3rem 0.8rem;
    border-radius: 12px;
    font-size: 0.85rem;
}

.ticket-body {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.ticket-qr img {
    width: 120px;
    height: 120px;
    border-radius: 10px;
}

.ticket-info p {
    margin: 0.2rem 0;
    color: #333;
    font-size: 0.95rem;
}
</style>