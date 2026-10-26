<script setup>
import { ref, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import QRCode from 'qrcode'

const route = useRoute()
const toast = inject('toast')
const order = ref(null)
const qrDataUrl = ref('')

onMounted(async () => {
    const { data } = await api.getOrder(route.params.id)
    order.value = data

    const qrText = `Заказ: ${data.order_number}\nEmail: ${data.email}\nСумма: ${data.total_price} ₽`
    qrDataUrl.value = await QRCode.toDataURL(qrText)

    // Уведомление показываем ЗДЕСЬ — после успешной загрузки заказа
    toast.value.show('Спасибо за покупку! 🎉')
})
</script>

<template>
    <div v-if="order" style="text-align: center; padding: 60px 20px;">
        <h1>✅ Заказ успешно оформлен!</h1>
        <p style="font-size: 18px; margin: 20px 0;">
            Номер вашего заказа: <strong>{{ order.order_number }}</strong>
        </p>
        <p>Билеты отправлены на email: {{ order.email }}</p>

        <div style="margin: 30px 0;">
            <img :src="qrDataUrl" alt="QR-код заказа" style="max-width: 250px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <p style="color: #666; margin-top: 10px; font-size: 14px;">
                Покажите этот QR-код на входе
            </p>
        </div>

        <router-link to="/" class="cta-button">Вернуться на главную</router-link>
    </div>
</template>