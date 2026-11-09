<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import TicketForm from '../components/TicketForm.vue'

const route = useRoute()
const concert = ref(null)
const loading = ref(true)

onMounted(async () => {
    try {
        const { data } = await api.getConcert(route.params.id)
        concert.value = data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div>
        <section v-if="loading" class="section">
            <p>Загрузка...</p>
        </section>

        <section v-else-if="concert" class="section">
            <div class="concert-card">
                <div class="concert-image">
                    <img :src="concert.artist.image" :alt="concert.artist.name">
                </div>

                <div class="concert-info">
                    <h3 class="concert-title">{{ concert.artist.name }}</h3>
                    <div class="detail-item">{{ concert.venue.city }}, {{ concert.venue.name }}</div>
                    <div class="detail-item">
                        {{ new Date(concert.start_time).toLocaleString('ru') }}
                    </div>
                    <div class="price-tag">
                        <strong class="price-amount">Цена: от {{ concert.min_price }} ₽</strong>
                    </div>
                </div>

                <TicketForm :concert="concert" />
            </div>
        </section>
    </div>
</template>