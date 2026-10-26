<script setup>
import { onMounted, ref } from 'vue'
import { useConcertsStore } from '../stores/concerts'
import { useUserStore } from '../stores/user'
import api from '../api'

const user = useUserStore()
const store = useConcertsStore()

const cities = ref([])
const genres = ref([])
const selectedCity = ref('')
const selectedGenre = ref('')

onMounted(async () => {
    store.fetchConcerts()
    store.fetchArtists()
    store.fetchVenues()

    try {
        const { data } = await api.getFilters()
        cities.value = data.cities
        genres.value = data.genres
    } catch (e) {
        console.error(e)
    }
})

async function applyFilters() {
    const params = {}
    if (selectedCity.value) params.city = selectedCity.value
    if (selectedGenre.value) params.genre = selectedGenre.value

    try {
        const { data } = await api.getConcertsFiltered(params)
        store.concerts = data
    } catch (e) {
        console.error(e)
    }
}

function getCityImage(venueName) {
    const map = {
        'Лужники': '/media/lychini.jpeg',
        'Ледовый дворец': '/media/spb.png',
        'Экспоцентр': '/media/ekb.jpg',
        'ВТБ Арена': '/media/vtb.jpg',
        'Live Arena': '/media/livearena.jpg',
    }
    return map[venueName] || '/media/concert.jpg'
}
</script>

<template>
    <section id="search" class="section">
        <div class="search-container">
            <div class="search-form">
                <input
                    v-model="store.searchQuery"
                    type="text"
                    placeholder="Введите артиста, город или площадку"
                    class="search-input"
                >
                <button
                    v-if="store.searchQuery"
                    class="clear-search"
                    @click="store.clearSearch()"
                >
                    Очистить
                </button>
            </div>

            <div v-if="store.searchQuery" class="search-info">
                Найдено: <strong>{{ store.searchResults.length }}</strong>
            </div>
        </div>
    </section>

    <section id="home" class="hero">
        <h1>Лучшие концерты именно в твоем городе</h1>
        <p>Билеты на выступления популярных артистов, фестивали и музыкальные события</p>
        <router-link to="/tickets" class="cta-button">Купить билеты</router-link>
    </section>

    <div class="filters">
        <select v-model="selectedCity" @change="applyFilters" class="filter-select">
            <option value="">Все города</option>
            <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
        </select>

        <select v-model="selectedGenre" @change="applyFilters" class="filter-select">
            <option value="">Все жанры</option>
            <option v-for="g in genres" :key="g" :value="g">{{ g }}</option>
        </select>
    </div>

    <section id="concerts" class="section">
        <div class="section-header">
            <h2 class="section-title">
                {{ store.searchQuery ? `Результаты поиска "${store.searchQuery}"` : 'Ближайшие концерты' }}
            </h2>
        </div>

        <div v-if="store.loading" class="no-results"><p>Загрузка...</p></div>

        <div v-else class="concerts-list">
            <div v-for="c in store.searchResults" :key="c.id" class="concert-item">
                <div class="concert-date">
                    <div class="date-day">{{ new Date(c.start_time).getDate() }}</div>
                    <div class="date-month">
                        {{ new Date(c.start_time).toLocaleString('ru', { month: 'short' }) }}
                    </div>
                </div>
                <div class="concert-info">
                    <div class="concert-title">{{ c.artist.name }}</div>
                    <div class="concert-description">{{ c.description }}</div>
                    <div class="concert-location">{{ c.venue.city }}, {{ c.venue.name }}</div>
                    <div class="concert-time">
                        {{ new Date(c.start_time).toLocaleTimeString('ru', { hour: '2-digit', minute: '2-digit' }) }}
                    </div>
                </div>
                <div class="concert-right-section">
                    <button
                        class="favorite-btn"
                        @click="user.toggleFavorite(c.id)"
                        :class="{ active: user.isFavorite(c.id) }"
                    >
                        {{ user.isFavorite(c.id) ? '❤️' : '🤍' }}
                    </button>
                    <div class="concert-price">от {{ c.min_price }} ₽</div>
                    <router-link :to="`/tickets#concert-${c.id}`" class="buy-button">
                        Купить билет
                    </router-link>
                </div>
            </div>

            <div v-if="!store.searchResults.length" class="no-results">
                <h3>Ничего не найдено</h3>
            </div>
        </div>
    </section>

    <section id="artists" class="section">
        <div class="section-header">
            <h2 class="section-title">Популярные артисты</h2>
        </div>
    
        <div class="artists-grid">
            <div v-for="a in store.artists" :key="a.id" class="artist-card-new">
                <div class="artist-image-wrapper">
                    <img :src="a.image" :alt="a.name" class="artist-img-new">
                </div>
                <div class="artist-content">
                    <h3 class="artist-name-new">{{ a.name }}</h3>
                    <p class="artist-genre">{{ a.genre || 'Музыка' }}</p>
                    <p class="artist-description">{{ a.description }}</p>
                </div>
            </div>
        </div>
    </section>

    <section id="cities" class="section">
        <div class="section-header">
            <h2 class="section-title">Площадки</h2>
        </div>

        <div class="cities-grid-5">
            <div v-for="v in store.venues" :key="v.id" class="city-card">
                <img :src="getCityImage(v.name)" :alt="v.city" class="city-img">
                <div class="city-overlay"></div>
                <div class="city-info">
                    <div class="city-name">{{ v.city }}</div>
                    <div class="city-events">{{ v.name }}</div>
                    <div class="city-events">Вместимость: {{ v.capacity }}</div>
                </div>
            </div>
        </div>
    </section>

    <section class="section ticket-section">
        <div class="ticket-info">
            <h1>Как приобрести билет</h1>
            <div class="steps">
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-text">Выберите концерт и место</div>
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-text">Оплатите онлайн</div>
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-text">Получите билет на email или прямо на сайте QR-кодом</div>
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-text">Приходите на концерт!</div>
                </div>
            </div>
        </div>
    </section>
</template>