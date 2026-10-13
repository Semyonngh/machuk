import { defineStore } from 'pinia'
import api from '../api'

export const useConcertsStore = defineStore('concerts', {
    state: () => ({
        concerts: [],
        artists: [],
        venues: [],
        loading: false,
        error: null,
        searchQuery: '',
    }),

    getters: {
        searchResults: (state) => {
            if (!state.searchQuery.trim()) return state.concerts
            const q = state.searchQuery.toLowerCase().trim()
            return state.concerts.filter(c =>
                c.artist.name.toLowerCase().includes(q) ||
                c.venue.city.toLowerCase().includes(q) ||
                c.venue.name.toLowerCase().includes(q) ||
                (c.description || '').toLowerCase().includes(q)
            )
        },
    },

    actions: {
        async fetchConcerts() {
            this.loading = true
            this.error = null
            try {
                const { data } = await api.getConcerts()
                this.concerts = data
            } catch (e) {
                this.error = 'Не удалось загрузить концерты'
                console.error(e)
            } finally {
                this.loading = false
            }
        },

        async fetchArtists() {
            try {
                const { data } = await api.getArtists()
                this.artists = data
            } catch (e) {
                console.error(e)
            }
        },

        async fetchVenues() {
            try {
                const { data } = await api.getVenues()
                this.venues = data
            } catch (e) {
                console.error(e)
            }
        },

        setSearchQuery(query) {
            this.searchQuery = query
        },

        clearSearch() {
            this.searchQuery = ''
        },
    },
})