import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        email: localStorage.getItem('userEmail') || '',
        name: localStorage.getItem('userName') || '',
        phone: localStorage.getItem('userPhone') || '',
        favorites: JSON.parse(localStorage.getItem('userFavorites') || '[]'),
    }),
    getters: {
        isLoggedIn: (state) => !!state.email,
    },
    actions: {
        login(email) {
            this.email = email
            localStorage.setItem('userEmail', email)
        },
        logout() {
            this.email = ''
            this.name = ''
            this.phone = ''
            this.favorites = []
            localStorage.removeItem('userEmail')
            localStorage.removeItem('userName')
            localStorage.removeItem('userPhone')
            localStorage.removeItem('userFavorites')
        },
        updateProfile(name, phone) {
            this.name = name
            this.phone = phone
            localStorage.setItem('userName', name)
            localStorage.setItem('userPhone', phone)
        },
        toggleFavorite(concertId) {
            const idx = this.favorites.indexOf(concertId)
            if (idx === -1) this.favorites.push(concertId)
            else this.favorites.splice(idx, 1)
            localStorage.setItem('userFavorites', JSON.stringify(this.favorites))
        },
        isFavorite(concertId) {
            return this.favorites.includes(concertId)
        },
    },
})