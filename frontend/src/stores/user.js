import { defineStore } from 'pinia'
import api from '../api'

export const useUserStore = defineStore('user', {
    state: () => ({
        email: localStorage.getItem('userEmail') || '',
        name: '',
        phone: '',
        favorites: [],
    }),
    getters: {
        isLoggedIn: (state) => !!state.email,
    },
    actions: {
        async login(email) {
            this.email = email
            localStorage.setItem('userEmail', email)
            await this.loadProfile()
        },
        async loadProfile() {
            if (!this.email) return
            try {
                const { data } = await api.getProfile(this.email)
                this.name = data.name || ''
                this.phone = data.phone || ''
                this.favorites = data.favorites || []
            } catch (e) {
                console.error(e)
            }
        },
        async updateProfile(name, phone) {
            this.name = name
            this.phone = phone
            await api.updateProfile(this.email, { name, phone, favorites: this.favorites })
        },
        async toggleFavorite(concertId) {
            const idx = this.favorites.indexOf(concertId)
            if (idx === -1) this.favorites.push(concertId)
            else this.favorites.splice(idx, 1)
            await api.updateProfile(this.email, { favorites: this.favorites })
        },
        isFavorite(concertId) {
            return this.favorites.includes(concertId)
        },
        logout() {
            this.email = ''
            this.name = ''
            this.phone = ''
            this.favorites = []
            localStorage.removeItem('userEmail')
        },
    },
})