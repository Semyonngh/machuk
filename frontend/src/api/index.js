import axios from 'axios'

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
})

export default {
    getConcerts() {
        return api.get('concerts/')
    },
    getConcert(id) {
        return api.get(`concerts/${id}/`)
    },
    searchConcerts(query) {
        return api.get('concerts/search/', { params: { q: query } })
    },
    getArtists() {
        return api.get('artists/')
    },
    getVenues() {
        return api.get('venues/')
    },
    getCategories() {
        return api.get('categories/')
    },
    getFilters() {
        return api.get('filters/')
    },
    getConcertsFiltered(params) {
        return api.get('concerts/', { params })
    },
    buyTicket(concertId, data) {
        const token = localStorage.getItem('accessToken')
        return api.post(`concerts/${concertId}/buy/`, data, {
            headers: token ? { Authorization: `Bearer ${token}` } : {}
        })
    },
    getOrder(orderId) {
        return api.get(`orders/${orderId}/`)
    },
    register(data) {
        return api.post('register/', data)
    },
    login(data) {
        return api.post('token/', data)
    },
    getProfile() {
        const token = localStorage.getItem('accessToken')
        return api.get('profile/', {
            headers: { Authorization: `Bearer ${token}` }
        })
    },
    updateProfile(data) {
        const token = localStorage.getItem('accessToken')
        return api.put('profile/update/', data, {
            headers: { Authorization: `Bearer ${token}` }
        })
    },
    getMyOrders() {
        const token = localStorage.getItem('accessToken')
        return api.get('my-orders/', {
            headers: { Authorization: `Bearer ${token}` }
        })
    },
    getMyTickets() {
        const token = localStorage.getItem('accessToken')
        return api.get('my-tickets/', {
            headers: { Authorization: `Bearer ${token}` }
        })
    },
    getMyFavorites() {
        const token = localStorage.getItem('accessToken')
        return api.get('my-favorites/', {
            headers: { Authorization: `Bearer ${token}` }
        })
    },
}