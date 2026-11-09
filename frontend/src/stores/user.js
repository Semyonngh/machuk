import { defineStore } from 'pinia'
import api from '../api'

export const useUserStore = defineStore('user', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken') || '',
        refreshToken: localStorage.getItem('refreshToken') || '',
        profile: null,
    }),

    getters: {
        isLoggedIn: (state) => !!state.accessToken,
    },

    actions: {
        async register(data) {
            await api.register(data)
        },

        async login(email, password) {
            const { data } = await api.login({ username: email, password })
            this.accessToken = data.access
            this.refreshToken = data.refresh
            localStorage.setItem('accessToken', data.access)
            localStorage.setItem('refreshToken', data.refresh)
            await this.loadProfile()
        },

        async loadProfile() {
            try {
                const { data } = await api.getProfile()
                this.profile = data
            } catch (e) {
                console.error(e)
            }
        },

async updateProfile(data) {
    const { data: updated } = await api.updateProfile(data)
    this.profile = updated
},

async toggleFavorite(concertId) {
    if (!this.profile) {
        await this.loadProfile()
        if (!this.profile) return
    }
    const favorites = [...(this.profile.favorites || [])]
    const idx = favorites.indexOf(concertId)
    if (idx === -1) {
        favorites.push(concertId)
    } else {
        favorites.splice(idx, 1)
    }
    this.profile = { ...this.profile, favorites }
    await this.updateProfile({ favorites })
},

        isFavorite(concertId) {
            if (!this.profile || !this.profile.favorites) return false
            return this.profile.favorites.includes(concertId)
        },

        logout() {
            this.accessToken = ''
            this.refreshToken = ''
            this.profile = null
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
        },
    },
})