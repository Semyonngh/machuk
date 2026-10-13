<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'

const route = useRoute()
const order = ref(null)

onMounted(async () => {
    const { data } = await api.getOrder(route.params.id)
    order.value = data
})
</script>

<template>
    <div>
        <h1>✅ Заказ оформлен</h1>
        <p v-if="order">Номер заказа: {{ order.order_number }}</p>
    </div>
</template>