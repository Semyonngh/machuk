<script setup>
import { onMounted } from 'vue'
import { useConcertsStore } from '../stores/concerts'
import TicketForm from '../components/TicketForm.vue'

const store = useConcertsStore()

onMounted(() => {
    store.fetchConcerts()
})
</script>

<template>
    <section class="tickets-section">
        <div class="container">
            <h1>Купить билеты</h1>
            <p>Выберите концерт и забронируйте места</p>

            <div
                v-for="c in store.concerts"
                :key="c.id"
                :id="`concert-${c.id}`"
                class="concert-card"
            >
                <div class="concert-image">
                    <img :src="c.artist.image" :alt="c.artist.name">
                </div>

                <div class="concert-info">
                    <h3 class="concert-title">{{ c.artist.name }}</h3>

                    <div class="concert-details">
                        <div class="detail-item">
                            {{ c.venue.city }}, {{ c.venue.name }}
                        </div>
                        <div class="detail-item">
                            {{ new Date(c.start_time).toLocaleString('ru', {
                                day: 'numeric',
                                month: 'long',
                                year: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            }) }}
                        </div>
                    </div>

                    <div class="price-tag">
                        <strong class="price-amount">
                            Цена: от {{ c.min_price }} ₽
                        </strong>
                    </div>
                </div>

                <TicketForm :concert="c" />
            </div>
        </div>
    </section>
</template>